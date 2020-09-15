#!/home/hannes/.local/share/miniconda/envs/bioinfo/bin/python3.8

################################################################################
# Author: Hannes Meinert                                                       #
# Last Modified: 11.08.2020                                                    #
################################################################################

############################## Procedure ####################################### 
# 1. convert absorption data to substrate conc
# 2. normalize (subtract blank)
# 3. make absolute
# 4. calculate activity

############################## Goals/ToDo ######################################
# Priority 1 (high)
## take most linear part separately for each sample (therefore display curve) then manual input display curve full and then each time after adjustment user decides when good


# Priority 2 (medium)
## make plot of activity curves prettier (average per sample, legend, blank)

# Priority 3 (low)
## function act_calc is confusing

############################## Import Modules ##################################
import argparse
import re
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from functions import process_std
from functions import process_info
from functions import abs_to_subconc
from functions import process_blank
from functions import act_calc
from functions import gen_output

############################## Initialize Argparser ############################
parser = argparse.ArgumentParser(
        description="This script is dedicated to help process absorption data "
                    + "generated with the Tecan. Therefore, the data in .xlsx "
                    + "format has to be converted into .csv and useless lines "
                    + "should be removed.")
parser.add_argument('-m', '--measurement', required=True,
                    help=".csv file containing measured CHI activities(rows) "
                    + "over desired time interval(row). First column gives "
                    + "name of sample (give replicates the same name)")
parser.add_argument('-i', '--info', required=True,
                    help="file containing per row the data for one sample "
                    + "white space separated.\ne.g.: C1 A1,A5,B6 1 1000\n"
                    + "(name wells conc_in_mg/mL dilution)")
parser.add_argument('-s', '--standard', required=True,
                    help=".out file generated with std_curve.py (contains "
                    + "lines with the following values starting with first "
                    + "line: slope (m), y-intercept (c), R² (r))")
parser.add_argument('-b', '--blank', required=True,
                    help=".csv file containing measured absorptions in rows "
                    + "over time and well number as first column. Each row is "
                    + "assumed to be a replicate.")
args = parser.parse_args()

############################## Process Input of Standard #######################
name = re.search(r'(\S*)_standard', str(args.standard))
name = name.group(1)
# read .out file containing data for standard curve
std_lin_reg = process_std(args.standard)
std_m = float(std_lin_reg[0])
std_c = float(std_lin_reg[1])
std_r = float(std_lin_reg[2])
# print equation and R**2
print(name + ' standard curve')
print('y = ' + str(std_m) + 'x + ' + str(std_c))
print('R**2 = ' + str(std_r))
print("\n")

############################## Process Input of Info File ######################
info_file = args.info
info_dict = process_info(info_file)

############################## Process Input of Measurement ####################
meas_df = pd.read_csv(args.measurement)
meas_df = meas_df.dropna(axis=1, how='all')
meas_df = meas_df.to_numpy()
meas_df = abs_to_subconc(meas_df, info_dict, std_m, std_c)
blank_file = args.blank
b_m = process_blank(blank_file, std_m, std_c)
summery_dict = act_calc(meas_df, info_dict, b_m, std_m, std_c)

############################## Generate Output #################################
gen_output(summery_dict, name)
