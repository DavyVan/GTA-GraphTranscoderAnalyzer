import Input
import IR
from scipy.sparse import csr_matrix

def graph_transcoder(args):
    _input: Input.input_base.InputBase = None
    _IR: csr_matrix = None

    # Instantiate input class
    if args.iformat == 'edgelist':
        _input = Input.InputEdgelist(args.inputfile, args.ibinary, args.comment, args.header, args.delimeter)
    
    # Process
    _input.read_from_file()
    _IR = _input.to_IR()
    _IR = IR.CSR.to_square_matrix(_IR)
