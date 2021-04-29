import argparse
import Input
import GraphTranscoder


def main():
    """Command line tool
    """
    # Parse arguments
    parser = argparse.ArgumentParser(description="GTA: Graph Transcoder & Analyzer")
    # input options
    inputgroup = parser.add_argument_group(title='Input options')
    inputgroup.add_argument('-i', '--input-file', type=str, required=True, dest='inputfile', help='Input file path')
    inputgroup.add_argument('-if', '--input-format', type=str, required=True, dest='iformat', choices=['edgelist'], help='Input file format')
    inputgroup.add_argument('-ib', '--input-binary', dest='ibinary', action='store_true', default=False, help='Input as binary')
    inputgroup.add_argument('-comment', type=str, default='#', help='Comment indicator in edgelist file. All lines start with designated character are ignored')
    inputgroup.add_argument('-header', action='store_true', default=False, help='Indicate if there is a header line in edgelist file (e.g. nv, ne)')
    inputgroup.add_argument('-delimeter', type=str, default='\s+', help='Column delimeter for edgelist file')
    # output options
    outputgroup = parser.add_argument_group(title='Output options')
    outputgroup.add_argument('-o', '--outputfile', type=str, required=True, dest='outputfile', help='Output file path')
    outputgroup.add_argument('-of', '--output-format', type=str, required=True, dest='oformat', choices=['metis'], help='Output file format')
    outputgroup.add_argument('-ob', '--output-binary', dest='obinary', action='store_true', default=False, help='Output as binary')
    # global options
    parser.add_argument('-v', '-V', '--version', action='version', version='GraphTranscoder 1.0.0')
    parsed_arg = parser.parse_args()
    print(parsed_arg)

    GraphTranscoder.GraphTranscoder(parsed_arg)


if __name__ == "__main__":
    main()
