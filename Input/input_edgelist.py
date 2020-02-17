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

        # Check file existence
        if not os.access(inputfile, os.R_OK):
            raise IOError('Input file is not accessable!')

    def read_from_file(self):
        self.edgelist = pd.read_csv(self.inputfile, delimiter=self.delimeter, header=(1 if self.has_header else None), comment=self.comment)

    def to_IR(self):
        edgelist_np = self.edgelist.values
        coo = coo_matrix((edgelist_np[:,0], (edgelist_np[:,0], edgelist_np[:,1])))
        self.CSR = coo.toscr()
        return self.CSR