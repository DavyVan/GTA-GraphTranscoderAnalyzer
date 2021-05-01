import Input
import Output
import IR
from scipy.sparse import csr_matrix
from typing import Optional
import argparse


def GraphTranscoder(args):
    _input: Optional[Input.InputBase] = None
    _IR: Optional[csr_matrix] = None
    _output: Optional[Output.OutputBase] = None

    # Instantiate input class
    if args.iformat == 'edgelist':
        _input = Input.InputEdgelist(args.inputfile, args.ibinary, args.comment, args.header, args.delimeter)
    else:
        raise NotImplementedError('Unknown input format!')
    
    # Process
    _input.read_from_file()
    _IR = _input.to_ir()
    _IR = IR.CSR.to_square_matrix(_IR)
    _IR = IR.CSR.symmetrify(_IR)

    # Instantiate output class
    if args.oformat == 'metis':
        _output = Output.OutputMetis(args.outputfile, args.obinary)
    else:
        raise NotImplementedError('Unknown output format!')

    # do output
    _output.write_to_file(_IR)
