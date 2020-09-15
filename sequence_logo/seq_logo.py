#!/home/hannes/.local/share/miniconda/envs/bioinfo/bin/python3.8

################################################################################
# Author: Hannes Meinert
# Last modified: 05.09.2020
################################################################################
# proper position labels
# proper coloring of glyphs
# estimate what happens when removing gaps
# mark important positions logo.highlight_position(p=i, color='', alpha=i)

############################## Import Modules ##################################
import logomaker as lm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse

############################## Initialize Argparser ############################
parser = argparse.ArgumentParser(
        description="Script to construct a sequence logo "
                  + "; the used length of the alignment is manually adjustable")
parser.add_argument('-a', '--aln', required=True,
                    help="alignment file in fasta format")
args = parser.parse_args()

############################## Functions #######################################
def gen_logo_and_plot(seqs, n, fig, ax, first, last):
    # generate df
    c_mat = lm.alignment_to_matrix(sequences=seqs,
                                   to_type='counts',
                                   characters_to_ignore='.-X')
    # remove gaped positions
    n_seqs = c_mat.sum(axis=1)
    pos_to_keep = n_seqs > len(seqs)/2
    c_mat = c_mat[pos_to_keep]
    c_mat.reset_index(drop=True, inplace=True)
    # convert to probability
    p_mat = lm.transform_matrix(c_mat,
                                from_type='counts',
                                to_type='probability')
    # generate logo
    logo = lm.Logo(df=p_mat, ax=ax[n], stack_order='small_on_top',
                   font_name='FreeSans', color_scheme=color_dict,
                   vsep=0.0005, vpad=0.005)
    # modify logo
    logo.ax.set_xticks([0, int(len(p_mat)/2), len(p_mat)])
    dif = last - first
    logo.ax.set_xticklabels([str(first), str(int(last - dif/2)), str(last)])
    logo.ax.set_ylabel('Probability')
    logo.style_spines(visible=False)
    logo.style_spines(spines=['left','bottom'], visible=True, linewidth=1)
    ## make glyphs invisible that have less than 10% probability
    logo.fade_glyphs_in_probability_logo(0.1,0.1000000001)

    return logo

############################## Code ############################################
# print available fonts
#print(lm.list_font_names())

# define colors for aminoacids
color_dict = {
        'AWFVGILPM':'black',
        'DE':'red',
        'KRH':'blue',
        'SCTYQN':'yellow'
}
# set range of alignment to be used
s = 1
e = 286

# read in sequence alignment
with open(args.aln) as in_aln:
    raw_seqs = in_aln.readlines()

# calculations number of subplots
dif = e - s
if dif%50 >= 25:
    n_plots = round(dif/50)
elif dif%50 == 0:
    n_plots = round(dif/50)
else:
    n_plots = round(dif/50) + 1

# generate list with boundaries for subplots
f_list = []
l_list = []
for n in range(n_plots):
    if n == 0:
        f_list.append(s)
        l = s + 50
        l_list.append(l)
    elif n + 1 == n_plots:
        f_list.append(l+1)
        l_list.append(e)
    else:
        f_list.append(l+1)
        l += 50
        l_list.append(l)

# generate figure and axis
fig, ax = plt.subplots(n_plots,figsize=[10,5])

# define matrix and plot for specified range
for n in range(n_plots):
    # remove headers and generate list of sequences in alignment format
    seqs = []
    for seq in raw_seqs:
        seq = seq.strip()
        if '#' not in seq and '>' not in seq:
            # range for sequence logo
            first = f_list[n]
            last = l_list[n]
            seq = seq[first:last]
            seqs.append(seq)
    logo = gen_logo_and_plot(seqs, n, fig, ax, first, last)

# print and save logo
logo.ax.set_xlabel('Position')
logo.fig.tight_layout()
plt.subplots_adjust(hspace=0.5)
plt.savefig(args.aln + '.png')
plt.show()

# clear current figure
plt.clf()
