#!/usr/bin/python3
import sys
import numpy as np
import matplotlib.pyplot as plt
import plot_tools as pt
pt.matplotlib_header()

dat = np.loadtxt(sys.argv[1])[1:]
dmin = dat.min()
print("Min: %f."%dmin)
dat -= dmin
plt.plot(dat)
plt.show()
