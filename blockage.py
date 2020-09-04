#!/usr/bin/python3
# -*- coding: utf-8 -*-
descr = """
Detects files, that shouldn't be compiled for qnx. When at least one such file is found, 
the script exits with an error. Otherwise it returns 0.
@author: ens3hi
"""

import os
import sys
import argparse
import blacklisting_lib
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../lib_py')
import file_lib
import parsing_lib

def get_dir_this():
    return os.path.dirname(os.path.realpath(__file__))
    
def get_path_json():
    return get_dir_this() + '/../../../build/qnx_target/release/bsot_prj_had/compile_commands.json'
    
def create_argparser():
    parser = argparse.ArgumentParser(description=descr)
    parser.add_argument('-b','--blacklist', required=True, help='Path to blacklist (lines of blacklisted files).')
    parser.add_argument('-f','--file', help='Optional path to compile_commands.json input file.', default=get_path_json())
    
    return parser

def main(args):
    file_lib.check_file('Options', args.file)
    file_lib.check_file('Blacklist', args.blacklist)
        
    sections = file_lib.extract_json_from_file(args.file)
    options = parsing_lib.json2options(sections)
    blacklist_lines = parsing_lib.read_blacklist_from_file(args.blacklist)
    is_blacklisted_found = blacklisting_lib.is_blacklisted_found(options, blacklist_lines)
    if is_blacklisted_found:
        print("Exiting with an error.")
        sys.exit(1)
    print("Exiting cleanly")

if __name__ == '__main__':
    parser = create_argparser()
    args = parser.parse_args()
    main(args)    