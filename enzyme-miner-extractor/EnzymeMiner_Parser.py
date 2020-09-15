#!/home/hannes/.local/share/miniconda/envs/bioinfo/bin/python3.8

################################################################################
# Author: Hannes Meinert                                                       #
# Last Modified: 15.07.2020                                                    #
################################################################################

############################## Import Modules ##################################
import pandas
import datetime

############################## Initialize Variables ############################
now = datetime.datetime.now()

#specify file with input() if necessery
filename = "EnzymeMiner Selection Table.xlsx"
xls = pandas.ExcelFile(filename)

############################## Process Data ####################################
#specify sheet with input()
sheetx = xls.parse('Full Dataset')
access = sheetx['Accession']
anno = sheetx['Annotation']
org = sheetx['Organism']
seq = sheetx['Sequence']
name = now.strftime("%y%m%d") + "_RESULTS.fasta"
try:
    with open(name, 'w') as f:
        n = 0
        while True:
            f.write(">" 
                    + str(access[n])
                    + " " 
                    + str(anno[n]) 
                    + " ["
                    + str(org[n])
                    + "]\n" 
                    + str(seq[n]) 
                    + "\n")
            n += 1
except IOError:
    print("An error occured while opening " + name + " for writing.")
    quit(1)

############################## Print Results ###################################
print("Results printed to " + name)

try:
    with open(name) as f:
	number = (sum(1 for _ in f))
except IOError:
    print("An error occured while opening " + name + " for reading.")
    quit(1)

num = int((number - 2) / 2)
print(str(num) + " sequences were extracted.")
