#!/usr/bin/python
#
# Lecture du fichier circuit
#

from __future__ import print_function
import csv
import collections
import matplotlib.pyplot as plt
import matplotlib.mlab
import re
#import subprocess
import json
#from dxfwrite import DXFEngine as dxf
import ConfigAgv

def tryConvertNum(s):
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return s

def ImportTrack(filename="../etc/circuit.trk"):
    sectionNames=[]
    section=''
    keys=[]
    sections = {}
    i=0
    
    try:
        trackFile = open(filename, "rb")
        reader = csv.reader(trackFile, delimiter='\t')
        for row in reader:
            if len(row) == 1 and row[0][0]=='[':
                section=row[0][1:-1]
                sectionNames.append(section)
                keys=[]
                sections[section]=[]
                continue
            if len(row) > 1 and section<>'' and keys==[]:
                keys=row
                Type=collections.namedtuple(section, keys)
                continue
            if len(row) > 1 and section<>'':
                values=[ tryConvertNum(s) for s in row ]
                sections[section].append(Type(*values))
                i=i+1
    except IOError:
        print("IOEROR:",filename)

    Datas=collections.namedtuple("Datas", sectionNames)
    datas = Datas( *[sections[section] for section in sectionNames ] )
    print(i,"track components imported.")
    return datas, sections

def exportJson():
    jsonDict=dict()
    for key in sections.keys():
        l=[d._asdict() for d in sections[key] ]
        jsonDict[key]=l
    f=file('out.json','w')
    f.write(json.dumps(jsonDict))

def plotDXFPoint(drawing, x,y,color,text):
    drawing.add(dxf.point((x,y), color=color))
    drawing.add(dxf.text(text, insert=(x,y), color=color, height=100.0))
    
def exportDXF(filename='output.dxf'):
    drawing = dxf.drawing(filename)
    for base in datas.BASE:
        plotDXFPoint(drawing, base.x, base.y, 7, base.name)
    for pc in datas.POINTCONNEXION:
        plotDXFPoint(drawing, pc.x, pc.y, 7, pc.name)
    drawing.save()
    
def GetDataInfoGlobales():
    return datas.GLOBALES[0]

''' @returns numAgv in configAgv.conf (15.10 or 15.03), -1 if error '''
def GetNumAgvFromConfigFile():
    numAgv = -1

    try:
        print(">=V15.10 ?")
        conf=dict()
        filename='../etc/configAgv.conf'
        try:
            file=open(filename)
            conf.update(json.load(file))
            file.close()
            print(filename,'... PARSED')
            try:
                numAgv=conf["Parameters"]["DataAgv"]["numAgv"]
            except:
                print('===')                            
        except IOError:
            print(filename,'... NOT FOUND')

    except:
        print("<=V15.03 ?")
        numAgv=-1
        f=open('../etc/configAgv.conf')        
        for line in f:
            m=re.match('(.*)typeAgvTh ,(.*)}', line)
            if m:
                numAgv=int(m.group(2))
                break
        f.close()

    return numAgv


def GetDataAgv():
    numAgv = GetNumAgvFromConfigFile()
    res = None

    print('numAgv=', numAgv)
    l=[agv for agv in datas.AGV if agv.numAgv == numAgv]

    if len(l)==1:
        return l[0]

    if len(datas.AGV) == 1:
        print("Only one agv in circuit.trk, NOT matching numAGV, anyway returns it !")
        return datas.AGV[0]

    print("Could not choose dataAgv, please help ...")
    for i in range(0, len(datas.AGV)):
        agv = datas.AGV[i]
        print(" ", i+1, " name:", agv.name, " numAgv:", agv.numAgv)
    
    n = int(input('Choice: '))

    return datas.AGV[n-1]    
        

def PlotBase():
    plt.figure('XY')
    for base in datas.BASE:
        plt.annotate(base.name,[base.x,base.y], color='black')

def PlotMagnet(plotLabels=True):
    plt.figure('XY')
    try:
      datas.MAGNET
    except AttributeError:
        print("well, no magnet at all !")
    else:
        if plotLabels:
            for magnet in datas.MAGNET:
                plt.annotate(magnet.name,[magnet.x,magnet.y], color='r')
        plt.plot([magnet.x for magnet in datas.MAGNET], [magnet.y for magnet in datas.MAGNET], 'o', label='Magnet', color='b')
    try:
      datas.TRANSPONDEUR
    except AttributeError:
        print("well, no transpondeur at all !")
    else:
        if plotLabels:
            for trans in datas.TRANSPONDEUR:
                plt.annotate(trans.name,[trans.x,trans.y], color='y')
        plt.plot([trans.x for trans in datas.TRANSPONDEUR], [trans.y for trans in datas.TRANSPONDEUR], 'o', label='trans', color='b')



def PlotTroncon():
    plt.figure('XY')
    for troncon in datas.TRONCON:
        idPcDebut=troncon.PCDebut
        idPcFin=troncon.PCFin
        pcDebut = [ pc for pc in datas.POINTCONNEXION if pc.ident==idPcDebut][0]
        pcFin = [ pc for pc in datas.POINTCONNEXION if pc.ident==idPcFin][0]
        plt.plot([pcDebut.x, pcFin.x], [pcDebut.y,pcFin.y], color='gray')

def PlotXY():
    plt.figure('XY')
    PlotMagnet()
    PlotTroncon()
    PlotBase()


def PrintInitBase():
    for base in datas.BASE:
        idBase = base.ident
        listAcc=[acc for acc in datas.ACCOSTAGE
            if acc.base == idBase]
        for acc in listAcc:
            if acc.initAssistee == 1:
                listPc = [ pc for pc in datas.POINTCONNEXION if pc.ident == acc.pointConnexion ]
                for pointConnexion in listPc:
                    #print("pc:", pc.name, " num:", pc.numPointConnnexion)
                    lbl = base.name + "\t" + str(pointConnexion.numPointConnexion)
                    print(lbl)

plt.ion()

print('---')
datas, sections = ImportTrack()
print("Track Importation OK.", len(datas), "sections available")
dataAgv=GetDataAgv()
print("Current AGV is", dataAgv.name)

