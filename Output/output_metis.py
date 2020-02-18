from .output_base import OutputBase
from scipy.sparse import csr_matrix

class OutputMetis(OutputBase):
    """Output adapter for metis format
        TODO: without weights now
    """
    def __init__(self, outputfile, is_binary):
        self.outputfile = outputfile
        self.is_binary = is_binary

    def to_target_format(self, csr: csr_matrix):
        pass

    def write_to_file(self, csr: csr_matrix):
        print('Writing to file in METIS format...')

        if not self.is_binary:
            fd = open(self.outputfile, "w")

            # header line with 2 parameters
            # METIS doesn't count a bidirection edge twice
            fd.write(str(len(csr.indptr)-1) + " " + str(len(csr.indices)//2))
            fd.write("\n")

            # vertices
            for i in range(len(csr.indptr)-1):
                # no vsize
                # no vwgt
                startIdx = csr.indptr[i]
                endIdx = csr.indptr[i+1]  # exclusive
                for j in range(startIdx, endIdx):
                    fd.write(str(csr.indices[j]+1) + " ")
                fd.write("\n")
            fd.write("\n")      # An extra \n is necessary to end file properly

            fd.close()
        else:
            raise NotImplementedError
