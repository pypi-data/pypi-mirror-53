"""command_line.py"""
import vbiz_parser
import sys
import getopt


def main():
    """main"""

    input_file = ''
    output_file = ''
    upload_path = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:u:", [
                                   "ifile=", "ofile=", "upath="])
    except getopt.GetoptError:
        print('Run vbiz_parser -h for helping')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('vbiz_parser -i <inputfile> -o <outputfile> -u <uploadpath>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg
        elif opt in ("-u", "--upath"):
            upload_path = arg

    vbiz_parser.let_parse(input_file, output_file, upload_path)
