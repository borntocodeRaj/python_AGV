#!/usr/bin/python
from math import *
import numpy

import matplotlib.pyplot as plt
import matplotlib.mlab

def carre(x):
	return x*x


def R(alpha, r0, gamma):
	alpha2=carre(alpha)
	alpha3=alpha*alpha2
	alpha4=alpha*alpha3
	
	return r0*(1+alpha2/2-alpha3/gamma+alpha4/(2*carre(gamma)))
	
def dRdAlpha(alpha, r0, gamma):
	alpha2=carre(alpha)
	alpha3=alpha*alpha2
	
	return r0*(alpha-3*alpha2/gamma+2*alpha3/carre(gamma))

def d2Rd2Alpha(alpha, r0, gamma):
	alpha2=carre(alpha)
	
	return r0*(1-6*alpha/gamma+6*alpha2/carre(gamma))

	
def Gamma(alpha, r0, gamma):
	r=R(alpha,r0,gamma)
	dr=dRdAlpha(alpha,r,gamma)
	
	return atan((r*cos(alpha)-dr*sin(alpha))/(r*sin(alpha)-dr*cos(alpha)))
	
def dSdAlpha(alpha, r0, gamma):
	r=R(alpha,r0,gamma)
	dr=dRdAlpha(alpha,r0,gamma)
	return sqrt(carre(r)+carre(dr))
	
def courbure(alpha, r0, gamma):
	r=R(alpha,r0,gamma)
	dr=dRdAlpha(alpha, r0, gamma)
	d2r=d2Rd2Alpha(alpha, r0, gamma)
	
	return abs((carre(r)+2*carre(dr)-r*d2r)/pow(carre(r)+carre(dr),1.5))
	
def phi(alpha, r0, gamma, empattement):
	return atan(courbure(alpha, r0, gamma)*empattement)
	

def ratio(gamma):
	aux=(1+carre(gamma)/32)
	return carre(aux)/(0.5+aux)


gamma=pi/2
empattement=2000
r0=4000

alphas=numpy.linspace(0,gamma,50)

plt.ion()
plt.figure()

c=courbure(gamma/2, r0, gamma)
r=1.0/c
rc=R(gamma/2, r0, gamma)
xc=(rc-r)*cos(gamma/2)
yc=(rc-r)*sin(gamma/2)
thetas=numpy.linspace(0,2*pi,100)
plt.plot([xc+r*cos(theta) for theta in thetas],[yc+r*sin(theta) for theta in thetas], label="Cmax", linestyle='-')
plt.plot([r0*cos(alpha) for alpha in alphas],[r0*sin(alpha) for alpha in alphas], label="Cercle", linestyle='--')

print "rc=",rc
print "r=",r


x=[]
y=[]
for alpha in alphas:
	r=R(alpha, r0, gamma)
	x.append(r*cos(alpha))
	y.append(r*sin(alpha))
plt.plot(x, y, label="Traj")


plt.grid(True)
plt.legend()
plt.axis('equal')

plt.figure()
plt.plot( alphas, [ R(alpha,r0,gamma) for alpha in alphas], label="r")
plt.plot( alphas, [ dRdAlpha(alpha,r0,gamma) for alpha in alphas], label="dRdAlpha")
plt.plot( alphas, [ d2Rd2Alpha(alpha,r0,gamma) for alpha in alphas], label="d2Rd2Alpha")
plt.plot( alphas, [ min([1.0/courbure(alpha,r0,gamma),10000]) for alpha in alphas], label="rayonInstantanne")
plt.grid(True)
plt.legend()

print R(gamma/2, r0, gamma)
print r0*(1+gamma*gamma/32)

plt.figure()
gammas=numpy.linspace(0,pi,50)
plt.plot( gammas, [ ratio(gamma) for gamma in gammas], label="ratio")
plt.grid(True)
plt.legend()

#phiMax=40*pi/180
phiMax=32*pi/180
#phiMax=35.06*pi/180
print "phiMax:",phiMax

cmax=tan(phiMax)/empattement
print "cmax:",cmax
rmax=1/cmax
print "rmax:",rmax

print 'rmax=', rmax
for gamma in [pi/6, pi/4, pi/3, pi/2, 2*pi/3, pi]:
	r0=rmax/ratio(gamma)
	print "gamma ", gamma, "rad ", gamma*180.0/pi, "deg ", 'r0', r0, "mm ",  ceil(r0/50)*50, " mm"
	#print 'verif:'
	#print phi(gamma/2, r0, gamma, empattement)*180/pi

rmax=3242
print 'r0=', rmax
for gamma in [pi/6, pi/4, pi/3, pi/2, 2*pi/3, pi]:
	r0=rmax/ratio(gamma)
	print "gamma ", gamma, "rad ", gamma*180.0/pi, "deg ", 'r0', r0, "mm ",  ceil(r0/50)*50, " mm"


fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot( [alpha*180/pi for alpha in alphas], [ rmax/ratio(alpha) for alpha in alphas], label="dmin")
ax.xaxis.set_ticks([0,30,45,60,90,120,180])
ax.grid(True)
plt.legend()


