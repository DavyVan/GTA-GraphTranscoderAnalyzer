import Input, Output
import IR
from scipy.sparse import csr_matrix


def graph_transcoder(args):
    _input: Input.input_base.InputBase = None
    _IR: csr_matrix = None
    _output: Output.output_base.OutputBase = None

    # Instantiate input class
    if args.iformat == 'edgelist':
        _input = Input.InputEdgelist(args.inputfile, args.ibinary, args.comment, args.header, args.delimeter)
    else:
        raise NotImplementedError('Unknown input format!')
    
    # Process
    _input.read_from_file()
    _IR = _input.to_IR()
    _IR = IR.CSR.to_square_matrix(_IR)
    _IR = IR.CSR.symmetrify(_IR)
    
    if args.oformat == 'metis':
        _output = Output.OutputMetis(args.outputfile, args.obinary)
    else:
        raise NotImplementedError('Unknown output format!')

    _output.write_to_file(_IR)
