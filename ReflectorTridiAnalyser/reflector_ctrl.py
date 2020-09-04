
import math
import re

###################################################################################################
class Measure:

    def __init__(self, x, y, intensity):
        self.x = x
        self.y = y
        self.intensity = intensity

###################################################################################################
def cleanMeasures(text):
    res = []
    rePoint = re.compile(r"\(([^,]+),([^,]+),([^)]+)\)")
    for x, y, intensity in rePoint.findall(text):
        res.append(Measure(float(x), float(y), float(intensity)))
    return res

###################################################################################################
def cleanTime(text):
    res1 = text.split("(")[0]
    res2 = res1.split("\t")
    return res2[0], res2[1], res2[2]

###################################################################################################
class displayManager:
    def __init__(self):
        self.__file = None
        self.__scans = {}
        self.__axes = None
        self.__hits = []
        self.__indexGraphNumCycle = []
        self.__indexGraphDate = []
        self.__currentScanIndex = 0

###################################################################################################
    def isReady(self):
        return self.__file is not None

###################################################################################################
    def loadFile(self, myFile):
        self.__file = myFile
        self.__scans = {}
        self.__indexGraphNumCycle = []
        self.__indexGraphDate = []

        with open(self.__file, "r") as aFileFd:
            for line in aFileFd:
                if len(line) > 1:
                    date, time, cycleNb = cleanTime(line)
                    scan = cleanMeasures(line)
                    self.__scans[cycleNb] = scan
                    self.__indexGraphNumCycle.append(cycleNb)
                    self.__indexGraphDate.append(date)
        self.__currentScanIndex = 0

###################################################################################################
    def setGraphAxes(self, axes):
        self.__axes = axes

###################################################################################################
    def getNbScan(self):
        return len(self.__indexGraphNumCycle)

###################################################################################################
    def getCurrentScanIndex(self):
        return self.__currentScanIndex

###################################################################################################
    def updateCurrentScanIndex(self, index):
        self.__currentScanIndex = index
        
###################################################################################################
    def filterScan(self, scan, coeff):
        newScan = {}
        k = 0            
        for i in range(0, len(scan)):
            newInt = 0.0
            for j in range(i-coeff, i+coeff+1):
                if j < 0:
                    l = 0
                elif j >= len(scan):
                    l = len(scan) - 1
                else:
                    l = j
                newInt += scan[l].intensity
            newInt /= (2 * coeff + 1)
            newScan[k] = Measure(scan[i].x, scan[i].y, newInt)
            k += 1
        return newScan
        
###################################################################################################
    def staticBinarizeScan(self, scan, seuil):
        newScan = {}            
        for i in range(0, len(scan)):
            if scan[i].intensity < seuil:
                newInt = 0
            else:
                newInt = 255
            newScan[i] = Measure(scan[i].x, scan[i].y, newInt)
        return newScan
        
###################################################################################################
    def dynamicBinarizeScan(self, scan, seuil):
        newScan = {}
        maxIntensity = 0
        for i in range(0, len(scan)):
            if scan[i].intensity > maxIntensity:
                maxIntensity = scan[i].intensity
                
        newScan = self.staticBinarizeScan(scan, maxIntensity - seuil)
        return newScan
        
###################################################################################################
    def computeReflectorLengthAndMiddle(self, scan):
        length = 0
        first = 0
        last = 0
        maxLen = 0
        middle = 0
        for i in range(0, len(scan)):
            if scan[i].intensity != 0:
                for j in range (i+1, len(scan)):
                    if scan[j].intensity == 0:
                        if (j - 1 - i ) > (last - first):
                            first = i
                            last = j - 1
                        break
                    elif j == len(scan)-1 & scan[j].intensity != 0:
                        first = i
                        last = j
                        maxLen = 1
                        break
                if maxLen == 1:
                    break
        length = math.fabs(scan[last].y - scan[first].y)
        middle = scan[first].y - length / 2
        return length, middle
                
###################################################################################################
    def getNbPointSupSeuil(self, scan, seuil):
        newScan = {}
        nbPoint = 0
        for i in range(0, len(scan)):
            if scan[i].intensity >= seuil:
                nbPoint += 1
        return nbPoint
        
###################################################################################################
    def processScan(self, scan, seuilBinarize, dynamicBinarize, coeffFilter):
        reflectorLen = 0
        middle = 0
        if coeffFilter != 0:
            scan = self.filterScan(scan, coeffFilter)
            
        if seuilBinarize != 0:
            if dynamicBinarize == 0:
                scan = self.staticBinarizeScan(scan, seuilBinarize)
            else:
                scan = self.dynamicBinarizeScan(scan, seuilBinarize)
                
            reflectorLen, middle = self.computeReflectorLengthAndMiddle(scan)
                
        return scan, reflectorLen, middle

###################################################################################################
    def draw(self, seuilBinarize, dynamicBinarize, coeffFilter):
        reflectorLen = 0
        index = self.__currentScanIndex
        cycleNb = self.__indexGraphNumCycle[index]
        date = self.__indexGraphDate[index]
        myFilteredScan = {}
        for h in self.__hits:
            h.remove()
        self.__hits = []
        self.__hits.extend(self.__axes.plot(0, 0, '.', color=(0, 0, 1, 1)))
        myScan = self.__scans[cycleNb]
        myScan, reflectorLen, middleRef = self.processScan(myScan, seuilBinarize, dynamicBinarize, coeffFilter)
        
        self.__hits.extend(self.__axes.plot(1500, middleRef, '.', color=(0, 0, 1, 1)))
            
        for i in range(0, len(myScan)):
            x = myScan[i].x
            y = myScan[i].y
            red = 0
            green = 1
            if myScan[i].intensity < seuilBinarize:
                red = 1
                green = 0
                
            self.__hits.extend(self.__axes.plot(x, y, '.', color=(red, green, 0, 1)))
            
        nbPointsSupSeuil = self.getNbPointSupSeuil(myScan, seuilBinarize)
        return nbPointsSupSeuil, cycleNb, date, reflectorLen, middleRef
    
