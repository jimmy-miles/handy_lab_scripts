#!/usr/bin/python3

################################################################################
# Author: Hannes Meinert                                                       #
# Last Modified: 24.05.2020                                                    #
################################################################################

# This script takes an input file containing DNA sequences
# in fasta format and converts those sequences into their respective complement
# or reverse or reverse-complement

import argparse

########## Define Arguments
parser = argparse.ArgumentParser(description="Parse DNA sequences from " 
                                 + "input filei in fasta format and convert.")             
parser.add_argument('-i', '--input', required=True, type=str,                                      
                    help="Specify the input file in fasta format.")
parser.add_argument('-c', '--conversion', 
                    required=True, 
                    type=str,
                    choices=['r', 'c', 'rc'],
                    help="Specify how to convert the sequences " 
                    + "'r' for reverse, "
                    + "'c' for complement, "
                    + "'rc' for reverse-complement.")
parser.add_argument('-o', '--out', required=True, type=str,                                          
                    help="Specify name of output file in fasta format.")    
args = parser.parse_args() 

########## Parse lines of file to define name and sequence
input_dict= {}
try:
    with open(args.input, 'r') as in_handle:
        for line in in_handle:
            line = line.strip()
            if line.startswith('>'):
                name = line.strip('>')
                input_dict[name] = ''
            else:
                line = line.strip('\n')
                input_dict[name] += line
except IOError:
    print("Error: Could not open/find " + args.input + ".")

########## Convert sequences
out_dict = {}
goes_in = 'ATGC'
goes_out = 'TACG'
translation = str.maketrans(goes_in, goes_out)
for header in input_dict:
    name = ">" + header
    if args.conversion == 'r':
        seq = input_dict[header][::-1]
    if args.conversion == 'c':
        seq = input_dict[header].translate(translation)
    if args.conversion == 'rc':
        seq = input_dict[header].translate(translation)
        seq = seq[::-1]
    out_dict[name] = seq

########## Print output to file
try:
    with open(args.out, 'w') as out_handle:
        for header in out_dict:
            out_handle.write(header + "\n" + out_dict[header] + "\n")
except IOError:
    print("Error: Could not open " + args.out + " for writing.")
