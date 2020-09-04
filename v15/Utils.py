from scipy import interpolate
import numpy
from math import *

#INTERPOLATION

""" @return linear interpolation of y over t assumed as time """
def InterpolateValue(t, y, ti):
	if ti < t[0]:
		return y[0]
	if ti > t[-1]:
		return y[-1]
	__f=interpolate.interp1d(t, y, bounds_error=False, fill_value=0, copy=False)
	return __f(ti).item()

""" @return continuous angle from angle in -pi/pi """
def ContinuousAngle(angle):
	res=[]
	prevAngle=angle[0]
	offset=0
	for anglei in angle:
		if anglei-prevAngle < -pi:
			offset=offset+2*pi
		if anglei-prevAngle > pi:
			offset=offset-2*pi
		res.append(anglei+offset)
		prevAngle=anglei
	return res

def __mod2pi(x):
	return ((x+pi) % (2*pi))-pi

def Mod2Pi(x):
	if isinstance(x,float) or isinstance(x,int):
		return __mod2pi(x)
	else:
		res=x
		for i in range(0,len(res)):
			res[i]=Mod2Pi(res[i])
		return res
#PLOT
''' format axe, add grid, label and axe line'''
def FormatAxe(ax, title, xlabel, ylabel):
	ax.axhline(linewidth=1, color='black')
	#ax.axvline(linewidth=1, color='black')  
	ax.legend()
	ax.grid(True)
	ax.set_title(title)
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)

#ARRAY
def AddArrayLine(array, line):
	if numpy.size(array) == 0:
		return numpy.array(line)
	else:
		return numpy.vstack((array,line))


#FILTER
def low_pass_filter(datas, fe=1.0/0.03, fc=0.5, initial_value=0):
	a = 1 / ( 1 + fe/fc)
	b = 1 / ( 1 + fc/fe)
	val = initial_value
	res = []
	for data in datas:
		val = a*data + b*val
		res.append(val)
	return res


#LOGS

''' Rescale to common time period
'''
def TimeRescale(list_datas):
	res = []

	print 'TimeRescale :'
	for datas in list_datas:
		print datas[0].timestamp, '\t-\t', datas[-1].timestamp

	tmin = numpy.max([datas[0].timestamp  for datas in list_datas if len(datas)>0 ])
	tmax = numpy.min([datas[-1].timestamp for datas in list_datas if len(datas)>0 ])
	min_len = len( list_datas[0].timestamp)
	for datas in list_datas:
		while datas.timestamp[0] <= tmin:
			datas = datas[1:]
		while datas.timestamp[-1] > tmax+0.01:
			datas = datas[0:-1]
		l=len(datas)
		if l < min_len :
			min_len = l
		res.append(datas)
	res2 = [ datas[0:min_len] for datas in res ]

	return res2

