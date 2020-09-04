#!/usr/bin/python
import matplotlib.mlab

dataDysf=[]

import json
import sys


class bcolors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

atLeastOneFileOK=0
currentArg=0
atLeastOneError=0
needToCreateJsonOutputFile=1
firstObjectInJson=1
firstDefaultInBaDysf=1
listId=[]
minLine=10


if len(sys.argv)<2:
	print bcolors.FAIL + bcolors.BOLD + "KO!! Usage: please put filename(s) as argument(s)" + bcolors.ENDC
	exit();


print "------------------------------------------------"
#create output file
fichierOut = open("dysf.json", "w")

for arg in sys.argv:
	if currentArg>0:
		print 'start with file : ' + arg + '...'
		try:
			f = open(arg,"r")
			lines = f.readlines()
			f.close()
			atLeastOneFileOK=1
		except:
			print bcolors.FAIL + bcolors.BOLD +'...Cannot open '+ arg +' -> check filename and path'+ bcolors.ENDC
			atLeastOneError=1
			continue
		try:
			f = open("/tmp/ba-dysf","w")
		except:
			print bcolors.FAIL + bcolors.BOLD +'ERROR : Cannot open tmp file'+ bcolors.ENDC
			atLeastOneError=1

		#modify initial file by deleting unusful lines and #-characters
		currentLine1 = 0
		for line in lines:
			if line.find("#IdStr") >= 0:
				line = line.replace("#", "")
				line = line.replace("(arretTraction,arretOutil,signalisation,rearmable,depannage) ", "")
				f.write(line)
				minLine=currentLine1
			if currentLine1>minLine:
				if currentLine1<(len(lines)-1):
					lsplit = line.split('\t')
					for i in range(len(lsplit)-1):
						f.write(lsplit[i] + '\t')
					typeLine = '"'+lsplit[len(lsplit)-1].replace('\n', '"\n')
					f.write(typeLine)
			currentLine1=currentLine1+1
		f.close()

		#start json format file
		if needToCreateJsonOutputFile:
			needToCreateJsonOutputFile=0
			fichierOut.write("{")

		#load previously built file
		dataDysf=matplotlib.mlab.csv2rec('/tmp/ba-dysf',delimiter='\t')

		currentLine = 0
		for i in dataDysf:
			if len(listId) > 0:
				if i.idstr in listId:
					continue
			#if not the first object
			if firstObjectInJson==0 :
				fichierOut.write(",")
			else:
				firstObjectInJson=0
			listId.append(i.idstr)
			fichierOut.write('\n\t"')
			fichierOut.write(i.idstr)
			fichierOut.write('": {')
			fichierOut.write('\n\t\t"Level":"')
			fichierOut.write(i.level)
			fichierOut.write('",\n\t\t"Description":"')
			fichierOut.write(i.decription) #in ba-dysf found decription instead of description (s is missing)
			fichierOut.write('",\n\t\t"Resolution_1":"')
			fichierOut.write(i.resolution)
			fichierOut.write('",\n\t\t"Famille":"')
			fichierOut.write(i.famille)
			fichierOut.write('",\n\t\t"Type":"')

			#in order not to have the first zero(s) deleted when writing as string in json file
			tmpType = str(i.type)
			for i in range(6-len(tmpType)):
				tmpType = str('0'+tmpType)

			fichierOut.write(str(tmpType))
			fichierOut.write('"\n\t}')
			currentLine=currentLine+1
	
		print '...done with file : ' + arg
	currentArg=currentArg+1


#end json format
if atLeastOneFileOK:
	fichierOut.write("\n}")

#close created file
fichierOut.close()
print "------------------------------------------------"
if atLeastOneError:
	print bcolors.WARNING + "WARNING : Some error(s) - check previous logs..." + bcolors.ENDC
	print "------------------------------------------------"
print bcolors.OKGREEN + bcolors.BOLD + "OK!! JOB terminated - Json file created as dysf.json" + bcolors.ENDC








