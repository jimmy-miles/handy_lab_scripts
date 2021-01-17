#!/home/hannes/.local/share/miniconda/envs/bioinfo/bin/python3.8

################################################################################
# Author: Hannes Meinert                                                       #
# Created: 08.12.2020                                                          #
# Last Modified: 14.12.2020                                                    #
################################################################################

############################## Tasks ###########################################
# 1. enable for .xml

############################## Import Modules ##################################
import argparse
import re

############################## Initialize Argparse #############################
parser = argparse.ArgumentParser(
        description="This script fetches sequences from a database file in "
                   + "fasta format. Therefore a tab separated input file is "
                   + "require with the accession number at the second position."
                   )
parser.add_argument('-i', '--input', required=True,
                    help="file with accession numbers")
parser.add_argument('-t', '--type', required=True,
                    help="dmnd: output from diamond search, tsv file with "
                        + "acc num at second position;; "
                        + "hmmer: modified output from hmmer, one acc num "
                        + "per line")
parser.add_argument('-d', '--db', required=True,
                    help="fasta file containing all sequences in the database")
parser.add_argument('-o', '--output', required=True,
                    help="name that is used for the output file in .fa format")
args = parser.parse_args()

############################## Process Data ####################################
# extract accession numbers from input file
acc_lst = []
data_dict = {}
if args.type == 'dmnd':
    with open(args.input, 'r') as in_file:
        for line in in_file:
            line = line.strip()
            p_lst = re.split('\t',line)
            acc_lst.append(p_lst[1])
elif args.type == 'hmmer':
    with open(args.input, 'r') as in_file:
        for line in in_file:
            line = line.strip()
            acc_lst.append(line)
else:
    print("The specified type is either not supported or does not exits.\n"
          + "See help for more information.")
    quit(1)
print("Accession numbers scanned.")

# extract sequences from database
total_seq = len(acc_lst)
count = 0
hit = ''
hit_check = False
with open(args.db, 'r') as db_file:
    for line in db_file:
        line = line.strip()
        if re.search('^>', line):
            if hit_check:
                print(str(count) + " of " + str(total_seq) + " fetched")
                hit_check = False
                data_dict[header] = hit
                hit = ''
            # quit when all sequences are fetched
            if count == total_seq:
                print('quit')
                break
            acc = re.split('\s', line)
            acc = acc[0]
            acc = acc.strip('>')
            for acc_num in acc_lst:
                if acc_num == acc:
                    count += 1
                    hit_check = True
                    header = line
                    break
        elif re.search(r'^[A-Z]', line) and hit_check:
            hit += line
print("Fetching sequences finished.")

############################## Generate Output File ############################
with open(args.output, 'w') as out_file:
    for header in data_dict.keys():
        out_file.write(header + '\n' + data_dict[header] + '\n')
