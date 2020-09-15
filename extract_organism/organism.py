#!/usr/bin/python3

################################################################################
# Author: Hannes Meinert
# Last Modification: 06.09.2020
# Version: 1.0
################################################################################

import re
import argparse

cdict = {}
odict = {}

############################## Initialize Argparser ############################
parser = argparse.ArgumentParser(
        description="Script to extract organism from fasta file and adjust "
                  + "a corresponding tree file if given.")
parser.add_argument('-i', '--input', required=True,
                    help="plain fasta file containing at least id and organism")
parser.add_argument('-t', '--treefile', help="treefile to be adjusted")
args = parser.parse_args()

############################# Scan File ########################################
with open(args.input, 'r') as handle:
    for line in handle:
        line = line.strip()
        if re.search(r'^>', line):
            match = re.search(r'^>(\S*)\s.*?\[(\w+\s?\w+\.?)(\s.*)?\]', line)
            org = match.group(2)
            cdict.setdefault(org, 0)
            cdict[org] += 1
            odict[match.group(1)] = org

############################## Sort Dictionary #################################
cdict = {k: v for k, v in sorted(cdict.items(), key=lambda item: item[1])}

############################## Print output ####################################
with open('organism_count.txt', 'w') as out_handle:
    for key in cdict.keys():
        out_handle.write(str(cdict[key]) + '\t' + key + '\n')
        
############################## Adjust Treefile #################################
if args.treefile != None:
    name = 'adjusted_' + str(args.treefile)
    with open(name, 'w') as out_handle:
        with open(args.treefile, 'r') as in_handle:
            for line in in_handle:
                for prot in odict.keys():
                    if re.search(prot, line):
                        line = re.sub(prot, prot + '[' + odict[prot] + ']', line)
                out_handle.write(line)
