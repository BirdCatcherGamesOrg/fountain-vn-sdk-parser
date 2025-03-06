import argparse

from vnparser.parser import FountainVNParser

if __name__ == '__main__':
    args = argparse.ArgumentParser(description='Process fountain files to VN SDK files')
    # TODO: Map this parameter onto a specific SDK. For now everything just goes through the string_table template.
    args.add_argument(
        '--sdk',
        help='Which VN SDK to parse for',
        required=False)
    args.add_argument(
        '--o',
        help='Output file',
        required=False)
    args.add_argument('file', type=str, help='fountain file')
    arg_values = args.parse_args()
    parser = FountainVNParser()
    parser.parse(arg_values.file, arg_values.o)
