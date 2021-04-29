from .OutputBase import OutputBase
from scipy.sparse import csr_matrix


class OutputMetis(OutputBase):
    """
    Output adapter for metis format (CSR).

    """
    def __init__(self, outputfile: str, is_binary: bool):
        self.outputfile = outputfile
        self.is_binary = is_binary

    def to_target_format(self, csr: csr_matrix):
        """
        This function is empty because the target format is the same as our ``IR`` (i.e. CSR).

        """
        pass

    def write_to_file(self, csr: csr_matrix) -> None:
        """
        This function only support non-binary file writing, otherwise it will raise ``NotImplementedError``.

        :param csr: The graph in CSR.
        :return: None
        """
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
            # TODO:
            raise NotImplementedError
