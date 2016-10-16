#!/usr/bin/python3
import sys
import pandas as pd
import matplotlib.pyplot as plt
import plot_tools as pt
pt.matplotlib_header()

dat = pd.read_fwf(sys.argv[1],skiprows=1,
    names = ["CYC","cycle","ETOT","totenergy","DETOT","energydiff","TST","wf","PX","wf2"])
dmin = dat['totenergy'].min()
print(dmin)
print("Min: %f."%dmin)
dat['totenergy'] -= dmin
plt.plot(dat['totenergy'])
plt.show()
