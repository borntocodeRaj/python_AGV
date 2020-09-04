
import math
import re
import sys
import matplotlib
import matplotlib.mlab

class Point:
    def __init__(self, x, y):
        self.x, self.y = x ,y
        
    def println(self):
        print "(%f, %f)" % (float(self.x), float(self.y))

def Import(filename):
	datas=matplotlib.mlab.csv2rec(filename,delimiter='\t')
	return datas
	
def extractScans(datas):
    scans = []
    for i in range(len(datas)):
        if str(datas[i].scan_y) == 'SizeScan':
            sizeOfScan = datas[i].scan_x
            startOfScan = int(i + 1);
            endOfScan = int(startOfScan + sizeOfScan);
            newScan = []
            for j in range(startOfScan, endOfScan):
                newScan.append(Point(datas[j].scan_x, datas[j].scan_y))
            scans.append(newScan)
            
    return scans

def extractRigid(datas):
    rigids = []
    for i in range(len(datas)):
        if str(datas[i].rigid_y) == 'SizeRigid':
            sizeOfRigid = datas[i].rigid_x
            startOfRigid = int(i + 1);
            endOfRigid = int(startOfRigid + sizeOfRigid);
            newRigid = []
            for j in range(startOfRigid, endOfRigid):
                newRigid.append(Point(datas[j].rigid_x, datas[j].rigid_y))
            rigids.append(newRigid)

    return rigids

def extractSmooth(datas):
    smooths = []
    for i in range(len(datas)):
        if str(datas[i].smooth_y) == 'SizeSmooth':
            sizeOfSmooth = datas[i].smooth_x
            startOfSmooth = int(i + 1);
            endOfSmooth = int(startOfSmooth + sizeOfSmooth);
            newSmooth = []
            for j in range(startOfSmooth, endOfSmooth):
                newSmooth.append(Point(datas[j].smooth_x, datas[j].smooth_y))
            smooths.append(newSmooth)

    return smooths
    
    

def getXScan(scan):
    x = []
    for i in scan:
        x.append(i.x)
    return x
    
def getYScan(scan):
    y = []
    for i in scan:
        y.append(i.y)
    return y

class displayManager:

    def __init__(self):
        self.__workingFile = None
        self.__datas = []
        self.__scans = []
        self.__rigidRec = []
        self.__smoothRec = []
        self.__points = None
        self.__axes = None
        self.__hits = []

        self.__currentFrame = 0

    def isReady(self):
        return self.__workingFile is not None

    def setworkingFile(self, workingFile):
        self.__workingFile = workingFile

    def loadFiles(self):
        self.__datas = []
        self.__scans = []
        self.__rigidRec = []
        self.__smoothRec = []
                           
        try:
            self.__datas = Import(self.__workingFile)
        except:
            print 'Error during loadFiles'
            sys.exit(2)
    
        self.__scans = extractScans(self.__datas)
        self.__rigidRec = extractRigid(self.__datas)
        self.__smoothRec = extractSmooth(self.__datas)
        self.__currentFrame = 0

    def setGraphAxes(self, axes):
        self.__axes = axes

    def getNbFrame(self):
        return len(self.__scans)

    def getCurentFrame(self):
        return self.__currentFrame
        
    def drawGraphInit(self):
        y0 = float(self.__rigidRec[0][1].y)
        x0 = float(self.__rigidRec[0][1].x)
        y2 = float(self.__rigidRec[0][3].y)
        x2 = float(self.__rigidRec[0][3].x)
        y3 = float(self.__rigidRec[0][4].y)
        x3 = float(self.__rigidRec[0][4].x)
        largeur = y3 - y0
        longueur = x2 - x0
        rigidRec1 = matplotlib.patches.Rectangle((y0,x0), largeur, longueur, color='red')
        
        y0 = float(self.__rigidRec[0][7].y)
        x0 = float(self.__rigidRec[0][7].x)
        y2 = float(self.__rigidRec[0][9].y)
        x2 = float(self.__rigidRec[0][9].x)
        y3 = float(self.__rigidRec[0][10].y)
        x3 = float(self.__rigidRec[0][10].x)
        largeur = y3 - y0
        longueur = x2 - x0
        rigidRec2 = matplotlib.patches.Rectangle((y0,x0), largeur, longueur, color='red')

        y0 = float(self.__smoothRec[0][0].y)
        x0 = float(self.__smoothRec[0][0].x)
        y2 = float(self.__smoothRec[0][2].y)
        x2 = float(self.__smoothRec[0][2].x)
        y3 = float(self.__smoothRec[0][3].y)
        x3 = float(self.__smoothRec[0][3].x)
        largeur = y3 - y0
        longueur = x2 - x0
        smoothRec = matplotlib.patches.Rectangle((y0,x0), largeur, longueur, color='orange')
        
        tim = matplotlib.patches.Circle((0,0), radius=50, color='green')

        x = getXScan(self.__scans[0])
        y = getYScan(self.__scans[0])
        
        self.__axes.add_patch(rigidRec1)
        self.__axes.add_patch(rigidRec2)
        self.__axes.add_patch(smoothRec)  
        self.__axes.add_patch(tim)
        self.__points = self.__axes.plot(y, x, '.', color='blue')[0]

    def drawGraph(self, index=0):
        self.__currentFrame = index
        
        x = getXScan(self.__scans[index])
        y = getYScan(self.__scans[index])
        self.__points.set_data(y, x)

