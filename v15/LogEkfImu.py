#!/usr/bin/python
import matplotlib.pyplot as plt
import matplotlib.mlab
import matplotlib
from math import *
import numpy as np
#PANDA
from pandas import DataFrame, read_csv
import pandas as pd #this is how I usually import pandas
from matplotlib.pyplot import savefig, grid
from cmath import pi
from sympy.physics.units import length
from scipy.spatial.distance import mahalanobis
from numpy import rad2deg

myFontSize=18
fig_path="plotImu.png"

ekf_imu_data=[]
ekf_variance_data=[]

def Import(filename):
    try:
        var=matplotlib.mlab.csv2rec(filename,delimiter='\t')
        print 'Import {0} OK, {1} values'.format(filename,len(var))
        return var
    except:
        print 'WARNING: Could not import {0}'.format(filename)
        return []

def PlotThetaDot(plotNb=1):
    plt.figure("theta dot",figsize=(13.,10.))
    plt.suptitle("$\dot{\\theta} [\degree.s^{-1}]$",fontsize=myFontSize)
    
    var = ekf_variance_data.p44.clip(min=0)
    sigma = np.sqrt(var)
    plt.plot(ekf_imu_data.timestamp, ekf_imu_data.thetadot, label="$\theta_dot$", linestyle="None", marker=".")
    plt.plot(ekf_variance_data.timestamp, 3*sigma, label="$3\sigma$", color="orange", linestyle="None", marker=".")
    plt.plot(ekf_variance_data.timestamp, -3*sigma, label="$3\sigma$", color="orange", linestyle="None", marker=".")
    
    grid(True)
    plt.legend()
    
    plt.show()
    savefig(fig_path)
    print("Saved at {0}".format(fig_path))
    

ekf_imu_data = Import("ekfImuTracer.txt")
ekf_variance_data = Import("ekfVariances.txt")