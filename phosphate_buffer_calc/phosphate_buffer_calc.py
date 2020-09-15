#!/home/hannes/.conda/envs/bioinfo/bin/python3.8

################################################################################
# Author: Hannes Meinert                                                       #
# Last Modified: 24.05.2020                                                    #
################################################################################

##constants
# pKa of NaH2PO4"
pKa = 7.21
HA = "NaH2PO4"
A = "Na2HPO4"

##intro messagees
print("Welcome to the phosphate buffer calculator!\n")
print("For the lazy-ones that don't want to calculate. :D\n")
print("calculates the amount of " + HA + " and " + A + " per liter.\n")

##user input pH and final conc
print("desired final concentration in mM\n")
cf = input("$ ")
print("desired pH\n")
pH = input("$ ")

##calculations
## pH=pKa+log(A/HA) ; c=A+HA 
ratio = 10 ** (float(pH) - pKa)
cHA = round(float(cf) / (1 + ratio), 4)
cA = round(float(cf) - cHA, 4)

##print results
print(str(cHA) + " mM of " + HA)
print(str(cA) + " mM of " + A)
