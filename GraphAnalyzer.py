"""
All routines in this file are implemented for ``CSR``.
"""

import Input
from scipy.sparse import csr_matrix
from typing import List, Union, Tuple
import numpy as np
from bisect import bisect_left
import tqdm
import threading


def degrees_undirected(csr: csr_matrix) -> List[int]:
    """
    Calculate the (in & out) degrees of every vertex.

    :param csr:
    :return:
    """

    row_start = csr.indptr
    nnodes = len(row_start) - 1

    degrees = np.zeros(nnodes)

    bar = tqdm.trange(nnodes)
    bar.set_description("Computing degrees")
    for i in bar:
        degrees[i] = row_start[i+1] - row_start[i]

    return list(degrees)


def count_triangles(csr: csr_matrix, degrees: List[int], locks: List[threading.Lock], triangle_dist: Union[np.ndarray, List[int]], global_result: List[int], global_result_lock: threading.Lock, start_v: int = 0, end_v: int = -1):
    """
    Count the number of triangles in the graph using the algorithm described in the Section 3.3 of
    `this paper <https://cs.stanford.edu/~rishig/courses/ref/l1.pdf>`_. Can also output the distribution of
    number of triangles for all vertices.

    :param csr: The graph in CSR.
    :return: Both of the total number of triangles and the number of triangles for every vertex.
    """

    row_start = csr.indptr
    edge_dst = csr.indices
    nnodes = len(row_start) - 1
    # degrees = degrees_undirected(csr)
    # triangle_dist = np.zeros(nnodes)
    result = 0

    if end_v == -1:
        end_v = nnodes

    bar = tqdm.trange(start_v, end_v)
    bar.set_description("Counting triangles")
    for i in bar:     # for each vertex
        # find qualified neighbours that:
        # 1. have degrees no less than the current vertex
        # 2. if degrees are equal, the higher ID wins
        N = []
        for edge in range(row_start[i], row_start[i+1]):
            neighbour = edge_dst[edge]
            if degrees[neighbour] > degrees[i]:
                N.append(neighbour)
            elif degrees[neighbour] == degrees[i]:
                if neighbour > i:
                    N.append(neighbour)

        # for each pair of neighbours, check for triangles
        for n1 in range(0, len(N)-1):
            N1 = N[n1]
            for n2 in range(n1+1, len(N)):
                N2 = N[n2]

                # only need to check if there is an edge between N1 and N2
                # by searching N2 in N1's neighbours
                found = bisect_left(edge_dst, N2, row_start[N1], row_start[N1+1])
                if found != row_start[N1+1] and edge_dst[found] == N2:      # triangle found
                    result += 1
                    locks[i].acquire()
                    triangle_dist[i] += 1
                    locks[i].release()
                    locks[N1].acquire()
                    triangle_dist[N1] += 1
                    locks[N1].release()
                    locks[N2].acquire()
                    triangle_dist[N2] += 1
                    locks[N2].release()

    global_result_lock.acquire()
    global_result[0] += result
    global_result_lock.release()


def count_triangles_mt(csr: csr_matrix, nthreads: int = 1) -> Tuple[int, List[int]]:
    nnodes = len(csr.indptr) - 1
    nnodes_per_thread = nnodes // nthreads
    threads = []
    locks = [threading.Lock() for i in range(nnodes)]
    total_count = [0]
    total_count_lock = threading.Lock()
    triangle_dist = np.zeros(nnodes)
    degrees = degrees_undirected(csr)
    for i in range(nthreads-1):
        threads.append(threading.Thread(target=count_triangles, args=(csr, degrees, locks, triangle_dist, total_count, total_count_lock, nnodes_per_thread * i, nnodes_per_thread * (i+1))))
    threads.append(threading.Thread(target=count_triangles, args=(csr, degrees, locks, triangle_dist, total_count, total_count_lock, nnodes_per_thread * (nthreads-1), nnodes)))

    for i in range(nthreads):
        threads[i].start()

    for i in range(nthreads):
        threads[i].join()

    return total_count[0], list(triangle_dist)
