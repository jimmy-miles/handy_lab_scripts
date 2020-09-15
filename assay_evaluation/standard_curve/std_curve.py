#!/home/hannes/.conda/envs/bioinfo/bin/python3.8

################################################################################ 
# Author: Hannes Meinert
# Last Modified: 04.08.2020
################################################################################ 

############################## Objectives ######################################
# better adjustment of axis limitations
# maybe add conc already in .csv file

############################## Import Modules ##################################
import argparse
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

############################## Initialize Argparser ############################
parser = argparse.ArgumentParser(
        description="This script is dedicated to help generate standard curves "
                    + "from absorption data measured with the Tecan. "
                    + "Therefore, the data in .xlsx "
                    + "format has to be converted into .csv and useless lines "
                    + "should be removed.")
parser.add_argument('-s', '--standard', required=True,
                    help=".csv file containing a standard curve "
                    + "for desired concentrations of the substrate.")
args = parser.parse_args()

############################## Functions #######################################
def identify_conc(std_df):
    ident_lst = []
    std_dict = {}
    print("Assuming all columns in the .csv file are replicates.")
    i_lst = std_df.iloc[0:, 0:1].values.tolist()
    for i in i_lst:
        ident_lst.append(i[0])
    for well in ident_lst:
        if well.isnumeric() or well.isalpha():
            # backup user input
            while True:
                print("Which substrate concentration is in the wells of row "
                      + well + "? (integer value in µM)")
                conc = input()
                try:
                    conc = float(conc)
                except ValueError:
                    continue
                break
            std_dict[well] = conc
    return std_dict

def process_std(std_df, std_dict, name):
    std_df['average abs'] = std_df.mean(1)
    std_df['conc in µM'] = std_dict.values()
    # calculate linear regression
    y = np.array(std_df['average abs'])
    x = np.array(std_df['conc in µM'])
    m, c, r, p, stderr = stats.linregress(x, y)
    lin_reg_tup = (m, c, r)
    # plot linear regression
    plt.figure(0)
    ax = plt.subplot(111)
    ax.plot(x, y, 'o', markersize=3, color='black')
    ax.plot(x, m*x + c, 'r', linestyle='--', color='gray')
    ## hide top and right axis
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ## set axis limitations
    plt.xlim(0, np.amax(x) + np.amax(x)*0.1)
    plt.ylim(0, round(np.amax(y), 0) + 0.5)
    ## plot R**2 and equation to plot
    plt.text(int(np.amax(x))*0.05, int(np.amax(y)) - 0.25,
             'y = ' + str(round(m, 4)) + '*x + ' + str(round(c, 4))
             + '\nR² = ' + str(round(r, 4)))
    ## set axis labels
    plt.xlabel('concentration in µM', fontsize=10)
    plt.ylabel('absorption at 384 nm', fontsize=10)
    ## generate output
    plt.savefig('linear-regression_' + name + '.png')
    print('y = ' + str(m) + 'x + ' + str(c))
    print('R**2 = ' + str(r))
    ## generate dict for lin_reg_data
    data_dict = {'m': str(m), 'c': str(c), 'r': str(r)}
    return data_dict
################################################################################

############################## Initialize Variables ############################
match = re.search(r'(.*)\.csv', args.standard)
name = match.group(1)

############################## Process Input ###################################
try:
    std_df = pd.read_csv(args.standard)
except IOError:
    print("Could not read " + args.standard + "!")
    quit(1)
std_df = std_df.dropna(axis=1, how='all')
std_dict = identify_conc(std_df)
data_dict = process_std(std_df, std_dict, name)

############################## Generate Output-File ############################
try:
    with open(name + '.out', 'w') as out_handle:
        out_handle.write(data_dict['m'] + '\n'
                         + data_dict['c'] + '\n'
                         + data_dict['r'])
except IOError:
    print("Could not open " + name + " for writing.")
