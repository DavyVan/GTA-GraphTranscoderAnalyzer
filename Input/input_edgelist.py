from .input_base import InputBase
import os
import pandas as pd
import numpy
from scipy.sparse import csr_matrix, coo_matrix

class InputEdgelist(InputBase):
    """Input adapter for edgelist file without weights
    """
    def __init__(self, inputfile, is_binary, comment='#', has_header=False, delimeter=' '):
        self.inputfile = inputfile
        self.is_binary = is_binary
        self.comment = comment
        self.has_header = has_header
        self.delimeter = delimeter
        self.edgelist: numpy.ndarray

        # Check file existence
        if not os.access(inputfile, os.R_OK):
            raise IOError('Input file is not accessable!')

    def read_from_file(self):
        print('Reading from edgelist...')
        self.edgelist = pd.read_csv(self.inputfile, delimiter=self.delimeter, header=(1 if self.has_header else None), comment=self.comment).values

    def to_IR(self):
        print('Reordering vertex ID...')
        self.reorder_vertex_id()

        print('Converting to CSR...')
        coo = coo_matrix((self.edgelist[:,0]+1, (self.edgelist[:,0], self.edgelist[:,1])))      # data cannot be zero
        self.CSR = coo.tocsr()

        del self.edgelist       # free memory
        return self.CSR

    """""""""""
    Edgelist specified functions
    """

    def reorder_vertex_id(self):
        """Force vertex ID starts from 1 and continuous
           This function should be called at the beginning at to_IR()
        """
        max_vid = numpy.amax(self.edgelist)
        v = numpy.zeros(max_vid+1, numpy.int64)

        # iterate all elements in edgelist, mark appeared vertex
        for element in numpy.nditer(self.edgelist):
            v[element] = 1
        
        # calculate vertex ID
        v_count = 0
        for i in range(0, max_vid+1):
            if v[i] == 1:
                v[i] = v_count
                v_count += 1

        # update vertex ID
        with numpy.nditer(self.edgelist, op_flags=['readwrite']) as it:
            for x in it:
                x[...] = v[x]