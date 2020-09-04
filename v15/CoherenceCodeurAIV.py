import LogCan20
import LogEncoder
from math import *
import Track
import numpy
import matplotlib.pyplot
import matplotlib.mlab


voie=Track.dataAgv.voie
empattement=Track.dataAgv.xTourelleAv-Track.dataAgv.xTourelleAr

dt=0.02
print 'dt=',dt

phiAvPrec=None

l_v1=[]
l_v2=[]
l_err=[]
t=[]

l_vArProj=[]
l_vPhi=[]
l_vw=[]

for i in range(0,15000):
	# BA
	phiAv = LogEncoder.codeurDirectionAv[i].position 
	phiAr = LogEncoder.codeurDirectionAr[i].position 
	vAr = LogEncoder.codeurTractionAr.vitesse_inst[i]
	# Gaussin 
	vAvG= LogCan20.datas[i].infrtlewheelspeedkphcent* ( 1000.0 * 1000 ) / ( 100 * 3600 )

	if phiAvPrec==None:
		dPhiAv_dt=0
	else:
		dPhiAv_dt=(phiAv-phiAvPrec)/dt

	# projection vitesse arriere sur axe x AGV
	# 1/2*(v2a+v2b) selon notation JB
	v2 = vAr*cos(phiAr)
	l_v2.append(v2)

	# projection vitesse avant sur axe x AGV
	# composante vitesse du codeur (v1bc1)
	vArProj = vAvG * cos(phiAv)
	l_vArProj.append(vArProj)
	# composante liee a la rotation de la tourelle
	vPhi = (voie/2.0) * dPhiAv_dt
	l_vPhi.append(vPhi)
	# composante liee a la roation du chariot
	# avec w=vAr*sin(phiAv-phiAr)/(empattement*cos(phiAv)))
	w=vAr*sin(phiAv-phiAr)/(empattement*cos(phiAv))
	vw = (voie / 2.0) * w
	l_vw.append(vw)
	# la projection, c'est la somme !
	v1 = vArProj + vPhi + vw
	l_v1.append(v1)	

	l_err.append(v1-v2)
	phiAvPrec=phiAv
	t.append(LogEncoder.codeurDirectionAv[i].timestamp)


matplotlib.pyplot.figure()
ax1 = matplotlib.pyplot.subplot(3,1,1)
ax1.plot(LogEncoder.codeurDirectionAv.timestamp,LogEncoder.codeurDirectionAv.position,label='phiAv')
ax1.plot(LogEncoder.codeurDirectionAr.timestamp,LogEncoder.codeurDirectionAr.position,label='phiAr')
ax1.legend()
ax1.grid(True)

ax2 = matplotlib.pyplot.subplot(3,1,2, sharex=ax1)
ax2.plot(t, l_v1, '-*', label='v1')
ax2.plot(t, l_v2, '-+', label='v2')
ax2.plot(t, l_vPhi, '-+', label='vPhi')
ax2.plot(t, l_vw, '-+', label='vw')
ax2.plot(LogEncoder.codeurTractionAr.timestamp, LogEncoder.codeurTractionAr.vitesse_inst, label='var')
ax2.plot(LogCan20.datas.timestamp, numpy.multiply(( 1000.0 * 1000 ) / ( 100 * 3600 ),LogCan20.datas.infrtlewheelspeedkphcent ), label='vavd')
ax2.legend()
ax2.grid(True)


ax3 = matplotlib.pyplot.subplot(3,1,3, sharex=ax1)
ax3.plot(t,l_err, label='erreur')
ax3.legend()
ax3.grid(True)
