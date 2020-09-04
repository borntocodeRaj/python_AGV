#!/usr/bin/python
import matplotlib.pyplot as plt
import matplotlib.mlab
import collections
import numpy


def Import(filename):
	datas=[]
	try:
		datas=matplotlib.mlab.csv2rec(filename,delimiter='\t')
		print "LogEncoder:", filename, "OK n=", len(datas)
	except:
		print filename, "empty file ?"
		datas=None
	return datas

def Import2(names):
	datas=[]
	for name in names:
		datas = Import(name)
		if datas != None :
			return datas
	return None

def Plot(datas):
	matplotlib.pyplot.figure()
	ax1 = matplotlib.pyplot.subplot(2,1,1)
	ax1.plot(datas.timestamp,datas.position, '-+', label='position')
	ax1.legend()
	ax1.grid(True)

	ax2 = matplotlib.pyplot.subplot(2,1,2, sharex=ax1)
	try:
	    ax2.plot(datas.timestamp,datas.vitesseinst,  '-+', label='vitesse inst')
	except:
            try:
        	ax2.plot(datas.timestamp,datas.vitesse_inst,  '-+', label='vitesse inst')
            except:
                print "End Vitesse instantannee"

	try:
	    ax2.plot(datas.timestamp,datas.vitessemoyenne,  '-+', label='vitesse moyenne')
	except:
            try:
	        ax2.plot(datas.timestamp,datas.vitesse_moyenne,  '-+', label='vitesse moyenne')
            except:
		print "End Vitesse moyenne"

	ax2.legend()
	ax2.grid(True)


def PlotAcc(datas):
	matplotlib.pyplot.figure()
	ax1 = matplotlib.pyplot.subplot(2,1,1)
	ax1.plot(datas.timestamp,datas.vitesseinst,  '-+', label='vitesse')
	ax1.legend()
	ax1.grid(True)

	ax2 = matplotlib.pyplot.subplot(2,1,2, sharex=ax1)
	dt = datas.timestamp[1:] - datas.timestamp[0:-1]
	acc = datas.vitesseinst[1:] - datas.vitesseinst[0:-1]
	acc = numpy.divide(acc, dt)
	ax2.plot(datas.timestamp[0:-1],acc,  '-+', label='acc_calc')

	if datas.dtype.fields.has_key("acceleration"):
		ax2.plot(datas.timestamp, datas.acceleration,  '-+', label='acc')

	if datas.dtype.fields.has_key("accelerationfiltree"):
		ax2.plot(datas.timestamp, datas.accelerationfiltree,  '-+', label='accfiltree')
	ax2.legend()
	ax2.grid(True)


def PlotAll():
	matplotlib.pyplot.figure()
	ax1 = matplotlib.pyplot.subplot(2,1,1)

	try:
		ax1.plot(codeurAvD.timestamp, codeurAvD.vitesseinst, label="AvD")
		ax1.plot(codeurAvG.timestamp, codeurAvG.vitesseinst, label="AvG")
	except:
		print "EndAvDG"

	try:
		ax1.plot(codeurTractionAv.timestamp, codeurTractionAv.vitesseinst, label="TractAv")
	except:
		print "EndAv"
       
        try :
            ax1.plot(codeurTractionArD.timestamp, codeurTractionArD.vitesseinst, label="TractArD")
            ax1.plot(codeurTractionArG.timestamp, codeurTractionArG.vitesseinst, label="TractArG")
        except:
	    print "EndTractArDG"


        try :
            ax1.plot(codeurTractionAvD.timestamp, codeurTractionAvD.vitesseinst, label="TractAvD")
            ax1.plot(codeurTractionAvG.timestamp, codeurTractionAvG.vitesseinst, label="TractAvG")
        except:
            print "EndTractAvDG"

	try:
		ax1.plot(codeurAvD.timestamp, codeurAvD.vitesseinst, label="AvD")
		ax1.plot(codeurAvG.timestamp, codeurAvG.vitesseinst, label="AvG")
	except:
		print "EndArDG"

	try:
		ax1.plot(codeurArD.timestamp, codeurArD.vitesseinst, label="ArD")
		ax1.plot(codeurArG.timestamp, codeurArG.vitesseinst, label="ArG")
	except:
		print "EndArDG"

	try:
		ax1.plot(codeurTractionAr.timestamp, codeurTractionAr.vitesseinst, label="TractAr")
	except:
		print "EndAr"
	ax1.legend()
	ax1.grid(True)
	ax1.set_title('vitesses codeurs traction')



	ax2 = matplotlib.pyplot.subplot(2,1,2, sharex=ax1)
	try:
		ax2.plot(codeurDirectionAv.timestamp, codeurDirectionAv.position, label="DirAv")
		ax2.plot(codeurDirectionAr.timestamp, codeurDirectionAr.position, label="DirAr")
	except:
		print "EndDir"

        try:        
            ax2.plot(codeurDirectionAvD.timestamp, codeurDirectionAvD.position, label="DirAvD")
            ax2.plot(codeurDirectionAvG.timestamp, codeurDirectionAvG.position, label="DirAvG")
        except:
            print "EndDirAvDG"


	ax2.legend()
	ax2.grid(True)
	ax2.set_title('angles codeurs directions')
	matplotlib.pyplot.show()

matplotlib.pyplot.ion()

codeurTractionAv=Import("codeurCodeurTractionAv.txt")
print "CodeurTractionAv OK"
codeurDirectionAv=Import("codeurCodeurDirectionAv.txt")
print "CodeurDirectionAv OK"
codeurDirectionAr=Import("codeurCodeurDirectionAr.txt")
print "CodeurDirectionAr OK"
codeurTractionAr=Import("codeurCodeurTractionAr.txt")
print "CodeurTractionAr OK"

codeurArD=Import("codeurCodeurArDroite.txt")
print "CodeurArDroite OK"
codeurArG=Import("codeurCodeurArGauche.txt")
print "CodeurArGauche OK"
codeurAvD=Import("codeurCodeurAvDroite.txt")
print "CodeurAvDroite OK"
codeurAvG=Import("codeurCodeurAvGauche.txt")
print "CodeurAvGauche OK"

codeurDirectionAvD=Import2(["codeurCodeurDirectionAvDroite.txt", "codeurCodeurDirectionAvantDroite.txt"])
print "codeurDirectionAvD OK"
codeurDirectionAvG=Import2(["codeurCodeurDirectionAvGauche.txt", "codeurCodeurDirectionAvantGauche.txt"])
print "codeurDirectionAvG OK"
codeurDirectionArD=Import2(["codeurCodeurDirectionArDroite.txt", "codeurCodeurDirectionArriereDroite.txt"])
print "codeurDirectionArD OK"
codeurDirectionArG=Import2(["codeurCodeurDirectionAvGauche.txt", "codeurCodeurDirectionArriereGauche.txt"])
print "codeurDirectionArG OK"

codeurTractionAvD=Import2(["codeurCodeurTractionAvDroite.txt", "codeurCodeurTractionAvantDroite.txt"])
print "codeurTractionAvD OK"
codeurTractionAvG=Import2(["codeurCodeurTractionAvGauche.txt", "codeurCodeurTractionAvGauche.txt"])
print "codeurTractionAvG OK"
codeurTractionArD=Import2( ["codeurCodeurTractionArDroite.txt", "codeurCodeurTractionArriereDroite.txt"])
print "codeurTractionArD OK"
codeurTractionArG=Import2(["codeurCodeurTractionArGauche.txt", "codeurCodeurTractionArriereGauche.txt"])
print "codeurTractionArG OK"

codeurLevage=Import("codeurCodeurMvtLevage.txt")
print "codeurLevage OK"
codeurRetract=Import("codeurCodeurMvtRetract.txt")
print "codeurRetract OK"
codeurLevageInitial=Import("codeurCodeurLevageInitial.txt")
print "codeurLevageInitial OK"
codeurTilt=Import("codeurCodeurMvtTilt.txt")
print "codeurTilt OK"
codeurTDL=Import("codeurCodeurMvtTDL.txt")
print "codeurTDL OK"


print "Import Done"
print "Use PlotT(param) function, with individual encoder as param to see encoder speed and position"
print "Use PlotAll() to see speeds of driving encoders and position of steering encoders"

