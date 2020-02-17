import numpy as np
from scipy.sparse import csr_matrix

def to_square_matrix(csr: csr_matrix) -> csr_matrix:
    """Make the input matrix into a square matrix according to its larger dimension
    
    Arguments:
        csr {csr_matrix} -- Input matrix
    
    Returns:
        csr_matrix -- Output matrix
    """
    print("Resizing...")
    maxDim = max(csr.get_shape())
    csr.resize((maxDim, maxDim))
    return csr      # Return even if csr can be modified by reference