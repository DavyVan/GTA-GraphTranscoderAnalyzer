from .InputBase import InputBase
import os
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix, coo_matrix
from typing import Optional, TextIO, Union, BinaryIO


class InputMetis(InputBase):
    """
    Input adapter for Metis format (CSR).

    """

    def __init__(self, inputfile: str, is_binary: bool = False, comment: str = '#'):
        """
        Initialize and check file access

        :param inputfile: Input file path.
        :param is_binary: Whether the file should be opened in binary mode.
        :param comment: The start character of comment lines in the file.
        """

        self.inputfile = inputfile
        self.is_binary = is_binary
        self.comment = comment
        self.CSR = None     # type: Optional[csr_matrix]
        self.fd = None      # type: Optional[Union[TextIO, BinaryIO]]

        # Check file existence
        if not os.access(inputfile, os.R_OK):
            raise IOError('Input file is not accessable!')

        if self.is_binary:
            raise NotImplementedError

    def read_from_file(self) -> None:
        """
        Read from Metis compatible file. Vertex numbering starts from 0.

        :return: None.
        """

        print('Reading from csr file...')
        self.fd = open(self.inputfile, 'r')

        line = self.readline_check()

        # read header
        header = [int(x) for x in line.split()]
        if len(header) < 2:
            print("The input file does not specify the number of vertices and edges.")
            exit(1)
        nnodes, nedges = header[:2]
        if len(header) == 3:
            fmt = header[2]
            if fmt > 0:
                print("Cannot read graph with weights right now.")
                exit(1)

        nedges *= 2     # double the number of edges due to undirected graph

        row_start = np.zeros(nnodes+1)
        edge_dst = np.zeros(nedges)
        e_wgt = np.ones(nedges)
        _nedges = 0

        # start reading
        for i in range(nnodes):
            line = self.readline_check()
            _edges = [int(x) for x in line.split()]
            for e in _edges:
                if e < 1 or e > nedges:
                    print("Edge %d for vertex %d is out of bound" % (e, i+1))
                    exit(1)
                if _nedges == nedges:
                    print("There are more edges in the file than specified.")
                    exit(1)
                edge_dst[_nedges] = e - 1       # the numbering starts from 0
                _nedges += 1
            row_start[i+1] = _nedges

        if _nedges != nedges:
            print("Edge number error")
            exit(1)
        elif _nedges*2 == nedges:
            print("Count (u,v) only once")
            exit(1)

        self.fd.close()

        self.CSR = csr_matrix((e_wgt, edge_dst, row_start))

    def to_ir(self) -> csr_matrix:
        """
        Do nothing.

        :return:
        """
        # TODO: reorder index
        return self.CSR

    def readline_check(self) -> str:
        """
        Read new line. Skip comments. Exit on premature end of file.

        :return: The new line
        """

        line = self.fd.readline()
        while line[0] == self.comment:
            line = self.fd.readline()
        if line == '':      # EOF
            print("Premature end of input file")
            exit(1)

        return line
