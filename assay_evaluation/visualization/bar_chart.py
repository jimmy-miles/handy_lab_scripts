#!/home/hannes/.local/share/miniconda/envs/bioinfo/bin/python3.8

################################################################################ 
# Author: Hannes Meinert
# Last Modified: 08.08.2020
################################################################################ 

############################## Objectives ######################################


############################## Import Modules ##################################
import argparse
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

############################## Initialize Argparser ############################
parser = argparse.ArgumentParser(
        description="This script is dedicated to plot activity data "
                   + "in a bar chart.")
parser.add_argument('-in', '--input', required=True,
                    help="text file containing average activity and std")
args = parser.parse_args()

############################## Processing Input ################################
# determine name
name = re.search(r'(\S*)_activity', str(args.input))
name = name.group(1)
# determine data for plot
label_lst = []
sact_lst = []
std_lst = []
try:
    with open(args.input, 'r') as in_handle:
        for line in in_handle:
            line = line.strip()
            if re.search(r'\S:', line):
                search_string = '(\S*):\ss\s=\s(\d*\.\d*)\s.*\s(\d*\.\d*)'
                hits = re.search(search_string, line)
                sample_sact = round(float(hits.group(2)), 2)
                sample_std = round(float(hits.group(3)), 2)
                label_lst.append(hits.group(1))
                sact_lst.append(sample_sact)
                std_lst.append(sample_std)
except IOError:
    print("Could not open " + args.input + " for reading.")
    quit(0)
x_max = round(max(sact_lst) + max(std_lst), -1)
x_max = 120

############################## Plot Data #######################################
# make evenly spaced array from length of label_lst
x = np.arange(len(label_lst))
# initialize plot
fig, ax = plt.subplots()
# set labels
ax.set_yticks(x)
ax.set_yticklabels(label_lst)
ax.set_xlabel('s in U/mg')
ax.set_title('CHI activity towards ' + name)
# set plot limits
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.set_xlim([0,x_max])
# plot bars
plt.barh(x, sact_lst, color='orange',
        xerr=std_lst, capsize=2.2)
# save plot and print to show
plt.savefig(name + '_activity_plot.png')
plt.show()
