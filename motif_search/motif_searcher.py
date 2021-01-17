#!/home/hannes/.local/share/miniconda/envs/bioinfo/bin/python3.8

################################################################################
# Author: Hannes Meinert                                                       #
# Created: 11.01.2021                                                          #
# Last Modified: 11.01.2021                                                    #
################################################################################

############################## Import Modules ##################################
import argparse
import re

############################## Initialize Argparse #############################
parser = argparse.ArgumentParser(
        description="This script searches a specified sequence motif in a "
                   + " set of protein sequences (.fa file).")
parser.add_argument('-i', '--input', required=True,
                    help=".fasta file which contains the protein sequence set.")
args = parser.parse_args()

############################## Print Sequence Length ###########################
name = str(args.input).split('.')
name = name[0]
seq_dict = {}
hit = ''
hit_check = False
with open(args.input, 'r') as in_file:
    for line in in_file:
        line = line.strip()
        if re.search('^>', line):
            if hit_check:
                seq_dict[acc] = hit
                hit = ''
                hit_check = False
            acc = line.strip('>')
        elif re.search(r'^[A-Z]', line):
            hit_check = True
            hit += line

############################## Find Motif ######################################
outname = name + '_motif_hits.fa'
print("Specify the motif you want to search for as a regex!")
motif_regex = input()
with open(outname, 'w') as out_file:
    for seq in seq_dict.keys():
        match = re.search(motif_regex, seq_dict[seq])
        if match: 
            print(seq)
            print(match.group())
            out_file.write('>' + seq + '\n')
            out_file.write(seq_dict[seq] + '\n')
print("Output generated to " + outname)
