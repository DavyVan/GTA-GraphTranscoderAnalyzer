"""
All routines in this file are implemented for ``CSR``.
"""

from scipy.sparse import csr_matrix
from typing import List, Tuple
import numpy as np
from bisect import bisect_left
import tqdm


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


def count_triangles(csr: csr_matrix) -> Tuple[int, List[int]]:
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
    degrees = degrees_undirected(csr)
    triangle_dist = np.zeros(nnodes)
    result = 0

    bar = tqdm.trange(nnodes)
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
                    triangle_dist[i] += 1
                    triangle_dist[N1] += 1
                    triangle_dist[N2] += 1

    return result, list(triangle_dist)
