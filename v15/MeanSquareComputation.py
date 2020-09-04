#!/usr/bin/python
import matplotlib.pyplot as plt
import matplotlib.mlab
from scipy import signal
from numpy import std, rad2deg

isHeadingHandled = False
myFontSize = 19
isSodebo = False
isShownInDegree=False

def Import(filename):
    try:
        var=matplotlib.mlab.csv2rec(filename,delimiter='\t')
        print 'Import {0} OK, {1} values'.format(filename,len(var))
        return var
    except:
        print 'WARNING: Could not import {0}'.format(filename)
        return []

def estimateStd(data, butterDim=2, butterWn=0.1):
    #dimention, frequency limit
    b,a = signal.butter(butterDim,butterWn)
    filteredData = signal.filtfilt(b,a,data)
    residual = data - filteredData
    return [filteredData, std(residual)]

#DATA IMPORT
xSensData = Import("CentraleInertielle.txt")
#EXEC
plt.ion()
plt.figure("Errors",figsize=(13.0,10.0))
plt.suptitle("Zero phase digital filtering for $\\sigma$ estimation",fontsize=myFontSize)
if isHeadingHandled:
    subplotNb = 2
else:
    subplotNb=1

subplotTab=[]
t = xSensData.timestamp

#OMEGA Z
omegaZ = xSensData.vitz
[filteredOmegaZ, stdOmegaZ] = estimateStd(omegaZ)
axOmegaZ=plt.subplot(subplotNb,1,1)
subplotTab.append(axOmegaZ)
if(isShownInDegree):
    axOmegaZ.plot(t,rad2deg(omegaZ),".",label="$\\omega_{z}$")
    axOmegaZ.plot(t,rad2deg(filteredOmegaZ),"r-",label="$Fil_{\\omega_{z}}$",linewidth=2.0)
else:
    axOmegaZ.plot(t,omegaZ,".",label="$\\omega_{z}$")
    axOmegaZ.plot(t,filteredOmegaZ,"r-",label="$Fil_{\\omega_{z}}$",linewidth=2.0)
axOmegaZ.set_xlabel("$time [s]$",fontsize=myFontSize)
if(isShownInDegree):
    axOmegaZ.set_ylabel("$\\omega_{z} [deg.s^{-1}]$",fontsize=myFontSize)
else:
    axOmegaZ.set_ylabel("$\\omega_{z} [rad.s^{-1}]$",fontsize=myFontSize)

axOmegaZ.text(.2,.1, "$\\sigma(\\omega_z)={0}$".format(stdOmegaZ),fontsize=myFontSize,
              horizontalalignment='center',
              verticalalignment='center',
              transform = axOmegaZ.transAxes)
axOmegaZ.text(.2,.2, "$V(\\omega_z) ={0}$".format(stdOmegaZ**2),fontsize=myFontSize,
              horizontalalignment='center',
              verticalalignment='center',
              transform = axOmegaZ.transAxes)
print("std_Dev_omegaZ= {0} rad \nsigma_omegaZ= {1} rad^2".format(stdOmegaZ,stdOmegaZ**2))
print("std_Dev_omegaZ= {0} degree \nsigma_omegaZ= {1} deg^2".format(rad2deg(stdOmegaZ),rad2deg(stdOmegaZ**2)))


# HEADING
if isHeadingHandled:
    heading = xSensData.yaw
    [filteredHeading, stdHeading] = estimateStd(heading)
    axHeading=plt.subplot(subplotNb,1,2)
    subplotTab.append(axHeading)
    axHeading.plot(t,heading,".",label="heading")
    axHeading.plot(t,filteredHeading,".",label="$Fil_{heading}$")
    axHeading.set_xlabel("$time [s]$")
    axHeading.set_ylabel("$heading [\\degree]$")
    axHeading.text(.2,.1, "$\\sigma_{\omega_z}$".format(stdHeading),fontsize=myFontSize,
                   horizontalalignment='center',
                   verticalalignment='center',
                   transform = axOmegaZ.transAxes)
    axHeading.text(4250,0.055, "$V(\\omega_z) ={0}$".format(stdHeading**2),fontsize=myFontSize,
                   horizontalalignment='center',
                   verticalalignment='center',
                   transform = axOmegaZ.transAxes)
    print("std_Dev{heading}= {0} rad \nsigma{heading}= {1} rad^2".format(stdHeading,stdHeading**2))
    print("std_Dev{heading}= {0} degree \nsigma{heading}= {1} deg^2".format(rad2deg(stdHeading),rad2deg(stdHeading**2)))

for subP in subplotTab:
    subP.legend()
    subP.grid(True)
