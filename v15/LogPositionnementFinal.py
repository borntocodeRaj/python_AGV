#!/usr/bin/python
import matplotlib.pyplot
import matplotlib.mlab


def read():
	datas=matplotlib.mlab.csv2rec("GT_PosFinal.txt", delimiter='\t')
	return datas

def plot(datas):
	matplotlib.pyplot.plot(datas.timestamp, datas.erreur, label="err")
	matplotlib.pyplot.plot(datas.timestamp, datas.consigne, label="cons")
	matplotlib.pyplot.plot(datas.timestamp, datas.mesure, label="mesure")
	matplotlib.pyplot.grid(True)
	matplotlib.pyplot.legend()
	matplotlib.pyplot.show()


datas=read()
plot(datas)

