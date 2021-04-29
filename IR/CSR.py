import numpy as np
from scipy.sparse import csr_matrix
import gc


class CSR:
    @staticmethod
    def to_square_matrix(csr: csr_matrix) -> csr_matrix:
        """
        Make the input matrix into a square matrix according to its larger dimension

        :param csr: Input matrix
        :return: Output matrix
        """

        print("CSR: Resizing...")
        maxDim = max(csr.get_shape())
        csr.resize(maxDim, maxDim)
        return csr      # Return even if csr can be modified by reference

    @staticmethod
    def symmetrify(csr: csr_matrix) -> csr_matrix:
        """
        csrT + csr, csr must be a square matrix. This function will need double memory space.

        :param csr: Input matrix
        :return: Output symmetric matrix
        """

        print('CSR: Symmetrifying...')
        csrT = csr.transpose()
        csr = csr + csrT

        gc.collect()
        return csr
