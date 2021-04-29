import Input
import GraphAnalyzer
from scipy.sparse import csr_matrix

_input = Input.InputMetis("E:/wiki-Talk.csr.txt", comment='%')
_input.read_from_file()
_CSR = _input.to_ir()

triangles, _ = GraphAnalyzer.count_triangles(_CSR)

print(triangles)