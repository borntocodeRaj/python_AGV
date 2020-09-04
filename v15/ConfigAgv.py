#!/usr/bin/python
#
# Lecture du fichier de configuration de l'AGV
#

from __future__ import print_function
import csv
import collections
import re
import json

# retrun dict object result of json reading of configAgv
def GetConfigAgv():
	conf=dict()
	file=open('../etc/configAgv.conf')
	conf.update(json.load(file))
	file.close()
	return conf

def GetNumAgv():
	if configAgv != None :
		return configAgv["Parameters"]["DataAgv"]["numAgv"]
	else: 
		return -1

try:
	configAgv = GetConfigAgv()
except:
	configAgv = None
	






