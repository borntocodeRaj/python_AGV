#!/usr/bin/python
# -*- coding: iso-8859-15 -*-


import collections
import sys
import re
import os
import csv
import matplotlib.mlab

###################################################################################################
def ImportFromCvs(filename):
    datas=matplotlib.mlab.csv2rec(filename,delimiter='\t')
    return datas
    
###################################################################################################
def checkDir(path):
    res=os.path.isdir(path)
    if not res:       
        print("The path \"%s\" is not a directory" % path)
    return res

###################################################################################################
def checkFile(path):
    res=os.path.isfile(path)
    if not res:       
        print("The path \"%s\" is not a file" % path)
    return res

###################################################################################################
def readline(s):
    if sys.version_info < (3, 0):
        return raw_input(s)
    else:
        return input(s)

###################################################################################################
def stringToList(mystr):
    return re.sub("[^\w|\.|-]", " ", mystr).split()

###################################################################################################
def tryConvertNum(s):
    if s == None:
        return s
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return s

###################################################################################################
def convertToFloat(s, defaultValue):
    try:
        return float(s)
    except ValueError:
        return float(defaultValue)
