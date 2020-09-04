#!/usr/bin/python
import matplotlib.pyplot
import matplotlib.mlab
import collections

def Import(filename):
	datas=[]
	try:
		datas=matplotlib.mlab.csv2rec(filename,delimiter='\t')
	except ValueError:
		print "empty file ?"
	print "LogEncoder:", filename, "OK n=", len(datas)
	return datas

def Plot():
	matplotlib.pyplot.figure()

	ax1 = matplotlib.pyplot.subplot(3,1,1)
	try:
		ax1.plot(datas.timestamp, datas.batractavg, label="BaAvG")
		ax1.plot(datas.timestamp, datas.batractavd, label="BaAvD")
		ax1.plot(datas.timestamp, datas.exttractavg, label="ICAvG")
		ax1.plot(datas.timestamp, datas.exttractavd, label="ICAvD")
#		ax1.plot(datas.timestamp, datas.coherencetractavg, label="ErrorAvG")
#		ax1.plot(datas.timestamp, datas.coherencetractavd, label="ErrorAvD")
		ax1.plot(datas.timestamp, datas.consbatractav,label="ConsBaTractionAv")
		ax1.plot(datas.timestamp, 100*datas.ctration,label="C_output*100")
	except:
		print "End Driving Front"

	ax1.legend()
	ax1.grid(True)
	ax1.set_title('codeurs traction avant')

	ax2 = matplotlib.pyplot.subplot(3,1,2, sharex=ax1)
	try:
		ax2.plot(datas.timestamp, datas.batractarg, label="BaArG")
		ax2.plot(datas.timestamp, datas.batractard, label="BaArD")
		ax2.plot(datas.timestamp, datas.exttractarg, label="ICArG")
		ax2.plot(datas.timestamp, datas.exttractard, label="ICArD")
#		ax2.plot(datas.timestamp, datas.coherencetractarg, label="ErrorArG")
#		ax2.plot(datas.timestamp, datas.coherencetractard, label="ErrorArD")
		ax2.plot(datas.timestamp, datas.consbatractar,label="ConsBaTractionAr")
		ax2.plot(datas.timestamp, 100*datas.ctration,label="C_output*100")
	except:
		print "End Driving Rear"

	ax2.legend()
	ax2.grid(True)
	ax2.set_title('codeurs traction arriere')

	ax3 = matplotlib.pyplot.subplot(3,1,3, sharex=ax1)
	try:
		ax3.plot(datas.timestamp, datas.badirav, label="BaAv")
		ax3.plot(datas.timestamp, datas.badirar, label="BaAr")
		ax3.plot(datas.timestamp, datas.extdirav, label="ICAv")
#		ax3.plot(datas.timestamp, datas.extdirar, label="ICAr")
#		ax3.plot(datas.timestamp, datas.coherencedirav, label="ErrorAv")
#		ax3.plot(datas.timestamp, datas.coherencedirar, label="ErrorAr")
		ax3.plot(datas.timestamp, datas.consbadirav, label="ConsBaDirectionAv")
		ax3.plot(datas.timestamp, datas.consbadirar, label="ConsBaDirectionAr")
		ax3.plot(datas.timestamp, datas.consgaussindirar, label="PVG-Ar")
		ax3.plot(datas.timestamp, datas.pid_p, label="PVG-Av")
#		ax3.plot(datas.timestamp, datas.pid_i, label="I")

	except:
		print "End Steering"

	ax3.legend()
	ax3.grid(True)
	ax3.set_title('codeurs direction')
	matplotlib.pyplot.show()

matplotlib.pyplot.ion()
	
try:
	datas=Import("InterControlManager.txt")
except IOError:
	print 'End InterControl Manager'

print "Import Done"
print "Use Plot() to see driving/steering order/encoder values"
