#!/home/hannes/.local/share/miniconda/envs/bioinfo/bin/python3.8

################################################################################
# Author: Hannes Meinert                                                       #
# Last Modified: 12.12.2020                                                    #
################################################################################

############################## Import Modules ##################################
import argparse
import re
import matplotlib.pyplot as plt


############################## Initialize Argparser ############################
parser = argparse.ArgumentParser(
        description="Visualize correlation of sequence length and number in "
                   + "given data set")
parser.add_argument('-f', '--fasta', required=True,
                    help="fasta file of sequence data set")
args = parser.parse_args()

############################## Process Data ####################################
len_dict = {}
seq_dict = {}
seq = ''
name = str(args.fasta).split('.')
name = name[0]
with open(args.fasta, 'r') as in_file:
    for line in in_file:
        line = line.strip()
        if re.search(r'^>', line):
            header = line
            if seq != '':
                seq_dict[header] = seq
                aa_count = 0
                for i in seq:
                    aa_count += 1
                len_dict.setdefault(aa_count, 0)
                len_dict[aa_count] += 1
            seq = ''
            continue
        else:
            seq += line

############################# Visualize Data ###################################
len_lst = list(len_dict.keys())
len_lst.sort()
x_max = round(len_lst[-1], -1)
x_min = round(len_lst[0], -1)
count = x_min
x_steps = []
while count < x_max:
    x_steps.append(count)
    count += 10
plt.hist(len_dict, bins=x_steps)
x_steps = []
count = 0
while count < x_max:
    x_steps.append(count)
    count += 250
plt.xticks(ticks=x_steps)
plt.show()

############################# Defining Thresholds###############################
print("Do you want to remove sequences that exceed a certain length threshold?")
print("(y/n)")
cont = input()
if cont == 'y':
    print("max length threshold:")
    max_len = int(input())
    print("min length threshold:")
    min_len = int(input())
else:
    quit(1)

############################# Process Data #####################################
out_dict = {}
for acc in seq_dict.keys():
    if len(seq_dict[acc]) >= min_len and len(seq_dict[acc]) <= max_len:
        out_dict.update({acc:seq_dict[acc]})

############################# Generate Output ##################################
out_name = name + '_' + str(min_len) + '-' + str(max_len) + '.fa'
with open(out_name, 'w') as out_file:
    for acc in out_dict.keys():
        out_file.write(acc + '\n' + out_dict[acc] + '\n')
print(out_name + " contains the remaining sequences.")
