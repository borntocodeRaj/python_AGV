import LogEncoder
import LogCan20

import matplotlib.pyplot
import matplotlib.mlab


matplotlib.pyplot.ion()
matplotlib.pyplot.figure()

matplotlib.pyplot.plot(LogCan20.datas.timestamp, LogCan20.datas.infrontangledegcent, label="infront")
matplotlib.pyplot.plot(LogCan20.datas.timestamp, LogCan20.datas.inrearangledegcent, label="inrear")

dirAv=LogEncoder.Import("codeurCodeurDirectionAv.txt")
dirAr=LogEncoder.Import("codeurCodeurDirectionAr.txt")

matplotlib.pyplot.plot(dirAv.timestamp, dirAv.position*180*100/3.14, label="inrear")

