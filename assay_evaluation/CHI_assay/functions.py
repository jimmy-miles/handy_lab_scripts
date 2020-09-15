############################## Import Modules ##################################
import pandas as pd
import numpy as np
import re
from scipy import stats
import matplotlib.pyplot as plt

############################## Define Functions ################################
# generate list containing data of standard curve
def process_std(standard_input_file):
    try:
        with open(standard_input_file, 'r') as in_handle:
            lin_reg_lst = []
            for line in in_handle:
                line = line.strip('\n')
                lin_reg_lst.append(line)
    except IOError:
        print("Could not open " + standard_input_file + " for reading.")
        quit(1)
    return lin_reg_lst

# generate info_dict containing information about the samples
def process_info(info_file):
    try:
        info_dict = {}
        with open(info_file, 'r') as in_handle:
            for line in in_handle:
                line = line.strip()
                items = re.split(' ', line)
                well_lst = re.split(',', items[1])
                info_dict[items[0]] = {'wells': well_lst,
                                       'conc': float(items[2]),
                                       'dil': float(items[3])}
    except IOError:
        print("Could not open " + args.info + " for reading.")
        quit(1)
    return info_dict

# calculate substrate concentration from absorption values
def abs_to_subconc(meas_df, info_dict, m, c):
    # find data series belonging to a sample
    for sample in info_dict.keys():
        for well in info_dict[sample]['wells']:
            i = np.where(meas_df == well)
            # convert absorption values to substrate concentration
            for row in meas_df[i[0]]:
                count = 1
                for el in row:
                    if type(el) != str:
                        conc = (el - c)/m
                        meas_df[i[0], count] = conc
                        count += 1
    return meas_df

# process blank to get slope
def process_blank(blank_file, std_m, std_c):
    blank_df = pd.read_csv(blank_file)
    blank_df = blank_df.to_numpy()
    # define x values
    i = np.where(blank_df == 'Time [s]')
    # fall-back for case that time per well is measured 
    if len(i[0]) == 0:
        b_arr = []
        i = np.where(blank_df == 'Time [ms]')
        # convert ms to s
        for row in blank_df[i[0]]:
            count = 1
            arr = []
            for el in row:
                if type(el) != str:
                    sec = el*0.001
                    arr.append(sec)
                    count += 1
            b_arr.append(arr)
        blank_x = np.vstack(b_arr)
        # make average for time
        av_lst = []
        for row in np.transpose(blank_x):
            av = sum(row) / len(row)
            av_lst.append(av)
        blank_x = np.transpose(np.array(av_lst))
    else:
        blank_x = np.array(blank_df[i[0]][0, 1:])
    # define y values
    arr = []
    for row in blank_df:
        if re.search(r'^[A-Z]\d\d?$', row[0]):
            arr.append(row[1:])
    if len(arr) < 2:
        blank_arr = np.array(arr)
    else:
        blank_arr = np.vstack(arr)
    count_r = 0
    for row in blank_arr:
        count_c = 0
        for el in row:
            if type(el) != str:
                conc = (el - std_c)/std_m
                blank_arr[count_r, count_c] = conc
            count_c += 1
        count_r += 1
    av_lst = []
    for row in np.transpose(blank_arr):
        av = sum(row) / len(row)
        av_lst.append(av)
    if len(av_lst) < 2:
        blank_y = np.transpose(np.array(av_lst))
    else:
        blank_y = np.transpose(np.vstack(av_lst))
    b_m, b_c, b_r, b_p, stderr = stats.linregress(blank_x.astype(float),
                                                  blank_y.astype(float))
    return b_m

# calculate average activity and standard deviation of each sample
def act_calc(meas_df, info_dict, b_m, std_m, std_c):
    act_dict = {}
    # m_lin defines most linear part from first point
    while True:
        print("How many time intervals you want to take for the "
              + "analysis? (most linear part from first to x)")
        m_lin = input()
        if m_lin.isnumeric() == True and int(m_lin) > 1:
            break
    m_lin = int(m_lin)
    # define volume per well
    while True:
        print("What is the volume per well? (in µL)")
        well_v = input()
        print("\n")
        if well_v.isnumeric() == True:
            break
    # define x values
    time = np.where(meas_df == 'Time [s]')
    # fall-back for case that time per well is measured 
    if len(time[0]) == 0:
        m_arr = []
        time = np.where(meas_df == 'Time [ms]')
        # convert ms to s
        for row in meas_df[time[0]]:
            arr = []
            count = 1
            for el in row:
                if type(el) != str:
                    sec = el*0.001
                    arr.append(sec)
                    count += 1
            m_arr.append(arr)
        x = np.vstack(m_arr)
        # make average for time values
        av_lst = []
        for row in np.transpose(x):
            av = sum(row) / len(row)
            av_lst.append(av)
        x = np.transpose(np.array(av_lst[0:m_lin]))
    else:
        x = meas_df[time[0]]
        x = np.array(x[0, 1:m_lin + 1])
    # process sample data
    for sample in info_dict.keys():
        e_conc = info_dict[sample]['conc']
        e_dil = info_dict[sample]['dil']
        e_conc = float(e_conc)/ (float(e_dil)*1000)
        for well in info_dict[sample]['wells']:
            i = np.where(meas_df == well)
            y = meas_df[i[0]]
            y = np.array(y[0, 1:m_lin + 1])
            m, c, r, p, stderr = stats.linregress(x.astype(float),
                                                  y.astype(float))
            print(sample + ' >R²' + str(r))
            # plot substrate decrease
            plt.figure(1, figsize=[10,5], frameon=False)
            plt.plot(x, y, 'x', markersize=2, label=sample)
            plt.plot(x, m*x + c, 'r', linestyle='--', color='gray')
            plt.savefig('activity_plot.png')
            # calculate specific activity
            m = abs(m - b_m)
            sact = (m*60*int(well_v)) / (10*1000000*float(e_conc))
            act_dict.setdefault(sample, [])
            act_dict[sample].append(sact)
    # calculate average specific activity per sample
    summery_dict = {}
    summery_dict['interval'] = m_lin
    for sample in act_dict.keys():
        av_sact = sum(act_dict[sample]) / len(act_dict[sample])
        print("average specific activity of " + sample + " = "
              + str(av_sact) + " U/mg")
        # calculate standard deviation per sample
        std = np.std(act_dict[sample])
        print("standard deviation for " + sample + ": +/-" + str(std))
        # generate summery_dict for output file
        summery_dict[sample] = {'av_sact': av_sact, 'std': std}
    return summery_dict

# process summery_dict to generate output file
def gen_output(summery_dict, name):
    try:
        with open(name + '_activity.out', 'w') as out_handle:
            out_handle.write('time interval from 1. to '
                             + str(summery_dict['interval'])
                             + '. was used for calculations.\n')
            for sample in summery_dict.keys():
                if sample == 'interval':
                    continue
                else:
                    out_handle.write(str(sample) + ': s = '
                                     + str(summery_dict[sample]['av_sact'])
                                     + ' +/- '
                                     + str(summery_dict[sample]['std']) + '\n')
    except IOError:
        print("Could not open activity.out for writing.")
        quit(1)
