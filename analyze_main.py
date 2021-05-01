import numpy as np

import Input
import GraphAnalyzer
from scipy.sparse import csr_matrix
import argparse
import matplotlib.pyplot as plt
import time


def ctriangles():
    _input = Input.InputMetis("E:/wiki-Talk.csr.txt", comment='%')
    _input.read_from_file()
    _CSR = _input.to_ir()

    nt = 8
    start = time.monotonic()
    triangles, _ = GraphAnalyzer.count_triangles_mt(_CSR, nthreads=nt)
    end = time.monotonic()

    print("Finished with %d threads in %.3f seconds, found %d triangles." % (nt, end-start, triangles))


def plot_degrees():
    # args
    parser = argparse.ArgumentParser(description="CDF Drawer.")
    parser.add_argument('-i', type=str, required=True, dest='inputfile', help='Input file path')
    parsed_arg = parser.parse_args()
    print(parsed_arg)

    _input = Input.InputMetis(parsed_arg.inputfile, comment='%')
    _input.read_from_file()
    _CSR = _input.to_ir()

    degrees = GraphAnalyzer.degrees_undirected(_CSR)

    # fig, ax = plt.subplots()
    # n, bins, patches = ax.hist(degrees, len(degrees), density=True, histtype='step', cumulative=True, label='CDF')
    # ax.grid(True)
    # # ax.legend(loc='right')
    # ax.set_title('CDF of degrees')
    # ax.set_xlabel('Degrees')
    # ax.set_ylabel('Occurrences')
    # ax.set_xscale("log")
    # # plt.show()
    # plt.savefig(parsed_arg.inputfile + ".cdf.pdf")


if __name__ == '__main__':
    ctriangles()
    # plot_degrees()
