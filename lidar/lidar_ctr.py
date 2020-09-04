
import math
import re


class Measure:

    def __init__(self, x, y, intensity):
        self.x = x
        self.y = y
        self.intensity = intensity


def cleanMeasures(text):
    res = []
    rePoint = re.compile(r"\(([^,]+),([^,]+),([^)]+)\)")
    for x, y, intensity in rePoint.findall(text):
        res.append(Measure(float(x), float(y), int(intensity)))
    return res


def cleanTime(text):
    res1 = text.split("(")[0]
    res2 = res1.split("\t")
    while res2.count(''):
        res2.remove('')
    return res2[-1]


class displayManager:

    def __init__(self):
        self.__workingFile = None
        self.__dicoMeasure = {}
        self.__axes = None
        self.__hits = []

        self.__indexGraph = []

        self.__curentFrame = 0

    def isReady(self):
        return self.__workingFile is not None

    def setworkingFile(self, workingFile):
        self.__workingFile = workingFile

    def loadFiles(self):
        self.__dicoMeasure = {}

        with open(self.__workingFile, "r") as aFileFd:
            for line in aFileFd:
                if len(line) > 1:
                    time = cleanTime(line)
                    measures = cleanMeasures(line)
                    self.__dicoMeasure[time] = measures
                    self.__indexGraph.append(time)
        self.__cuurentFrame = 0

    def setGraphAxes(self, axes):
        self.__axes = axes

    def getNbFrame(self):
        return len(self.__indexGraph)

    def getCurentFrame(self):
        return self.__curentFrame

    def drawGraph(self, index=None):
        if index is None:
            index = self.__curentFrame
        else:
            self.__curentFrame = index
        time = self.__indexGraph[index]
        for h in self.__hits:
            h.remove()
        self.__hits = []
        self.__hits.extend(self.__axes.plot(0, 0, '.', color=(0, 0, 1, 1)))
        for m in self.__dicoMeasure[time]:
            x = m.x
            y = m.y
            i = m.intensity / 255.
            vi = (math.exp(10 * i) - 1) / (math.exp(10) - 1)
            self.__hits.extend(
                self.__axes.plot(x, y, '.', color=(max(0, 1 - vi), min(1, vi), 0, 1)))
