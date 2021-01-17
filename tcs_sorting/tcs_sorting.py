#!/home/hannes/.local/share/miniconda/envs/bioinfo/bin/python3.8

################################################################################
# Author: Hannes Meinert                                                       #
# Created: 17.12.2020                                                          #
# Last Modified: 17.12.2020                                                    #
################################################################################

############################## Import Modules ##################################
import argparse
import re

############################## Initialize Argparser ############################
parser = argparse.ArgumentParser(
        description="Remove sequences from alignment "
                    + "with worse TCS than average TCS.")
parser.add_argument('-i', '--input', required=True,
                    help="alignment file in fasta format")
parser.add_argument('-s', '--score', required=True,
                    help="TCS file in ascii format")
args = parser.parse_args()

############################## Process TCS Input ###############################
s_dict = {}
name = str(args.input).split('.')
name = name[0]
with open(args.score, 'r') as s_file:
    for line in s_file:
        line = line.strip()
        if re.search('^SCORE', line):
            s_avg = line.split('=')
            s_avg = s_avg[1]
        if re.search('^cons', line):
            break
        if re.search('^\S*\s*:', line):
            hit = line.split(':')
            seq_acc = hit[0].strip()
            s_seq = hit[1].strip()
            s_dict[seq_acc] = s_seq

############################## Define bad Sequences ############################
bad_lst = []
for seq_acc in s_dict.keys():
    if int(s_dict[seq_acc]) < int(s_avg):
        bad_lst.append(seq_acc)
bad_seq_count = len(bad_lst)
print(str(bad_seq_count) + " sequences identified with lower average TCS than "
      + "average TCS of whole alignment.")

############################## Process Alignment ###############################
with open(name + '_edit.aln', 'w') as out_file:
    with open(args.input, 'r') as a_file:
        for line in a_file:
            line = line.strip()
            if re.search('^>', line):
                bad = False
                for seq_acc in bad_lst:
                    if re.search(seq_acc, line):
                        bad_lst.pop(bad_lst.index(seq_acc))
                        bad = True
                        break
                if not bad:
                    out_file.write(line + '\n')
            elif re.search('^[A-Z]|-', line) and not bad:
                out_file.write(line + '\n')

############################## Generate adjusted Fasta #########################
with open(name + '_edit.aln', 'r') as aln_file:
    with open(name + '_edit.fa', 'w') as fa_file:
        for line in aln_file:
            line = line.strip()
            if re.search('^>', line):
                fa_file.write(line + '\n')
            elif re.search('^[A-Z]|-', line):
                line = line.replace('-', '')
                fa_file.write(line + '\n')
