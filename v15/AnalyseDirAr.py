import LogCan20
import numpy
import LogMouvement
import LogEncoder

LogCan20.Plot()
LogCan20.matplotlib.pyplot.plot(LogEncoder.codeurDirectionAr.timestamp, numpy.multiply(LogEncoder.codeurDirectionAr.position,100.0*180/3.1415), label='codeurBA')

LogCan20.matplotlib.pyplot.plot(LogCan20.datas.timestamp, LogCan20.datas.outrearangledegcent, label='cdeposar')

p=LogCan20.datas.infrontleftwheelspeedkphcent

i=LogCan20.datas.infrontrightwheelspeedkphcent

LogCan20.matplotlib.pyplot.plot(LogCan20.datas.timestamp,i, label='i')

LogCan20.matplotlib.pyplot.plot(LogCan20.datas.timestamp,p, label='p')

LogCan20.matplotlib.pyplot.legend()
