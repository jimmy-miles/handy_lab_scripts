#!/home/hannes/.local/share/miniconda/envs/bioinfo/bin/python3.8

################################################################################
# Author: Hannes Meinert                                                       #
# Created: 17.12.2020                                                          #
# Last Modified: 17.12.2020                                                    #
################################################################################

############################## Import Modules ##################################
import argparse
import re

############################## Initialize Argparse #############################
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', required=True)
args = parser.parse_args()

############################## Print Sequence Length ###########################
seq_dict = {}
hit = ''
hit_check = False
with open(args.input, 'r') as db_file:
    for line in db_file:
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

for seq in seq_dict.keys():
    print(seq)
    print(len(seq_dict[seq]))
