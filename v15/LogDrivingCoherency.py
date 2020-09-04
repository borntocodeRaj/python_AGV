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
		ax1.plot(variateurCanSauer.timestamp, variateurCanSauer.batractard, label="BaArD")
		ax1.plot(variateurCanSauer.timestamp, variateurCanSauer.batractarg, label="BaArG")
		ax1.plot(variateurCanSauer.timestamp, variateurCanSauer.sauervitavg, label="SauerAvG")
		ax1.plot(variateurCanSauer.timestamp, variateurCanSauer.errtractfilt, label="ErreurTraction")
		ax1.plot(variateurCanSauer.timestamp, variateurCanSauer.vitrotationchassis, label="VitesseRotationChassis")
	except:
		print "End Driving Coherency"

	ax1.legend()
	ax1.grid(True)
	ax1.set_title('coherence codeurs traction')

	ax2 = matplotlib.pyplot.subplot(3,1,2, sharex=ax1)
	try:
		ax2.plot(variateurCanSauer.timestamp, variateurCanSauer.badirav, label="BaDirAv")
		ax2.plot(variateurCanSauer.timestamp, variateurCanSauer.sauerangleav, label="SauerDirAv")
		ax2.plot(variateurCanSauer.timestamp, variateurCanSauer.errdiravfilt, label="ErreurDirAv")
	except:
		print "End Front Steering Coherency"

	ax2.legend()
	ax2.grid(True)
	ax2.set_title('coherence codeurs direction avant')

	ax3 = matplotlib.pyplot.subplot(3,1,3, sharex=ax1)
	try:
		ax3.plot(variateurCanSauer.timestamp, variateurCanSauer.badirar, label="BaDirAr")
		ax3.plot(variateurCanSauer.timestamp, variateurCanSauer.saueranglear, label="SauerDirAr")
		ax3.plot(variateurCanSauer.timestamp, variateurCanSauer.errdirarfilt, label="ErreurDirAr")
	except:
		print "End Rear Steering Coherency"

	ax3.legend()
	ax3.grid(True)
	ax3.set_title('coherence codeurs direction arriere')
	matplotlib.pyplot.show()

matplotlib.pyplot.ion()
	
try:
	variateurCanSauer=Import("VariateurCanSauer.txt")
except IOError:
	print 'End Coherency Controler'

print "Import Done"
print "Use Plot() to see driving/steering coherency control"
