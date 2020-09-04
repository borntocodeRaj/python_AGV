#!/usr/bin/python
from dxfwrite import DXFEngine as dxf
import csv
import sys

if len(sys.argv) != 3:
	print "needs 2 args: input file (csv) and outpout file (dxf)"
	sys.exit(-1)

inputFile = sys.argv[1]
outputFile = sys.argv[2]

file = open(inputFile, "rb")
drawing = dxf.drawing(outputFile)
i = 0

try:
    reader = csv.reader(file, delimiter='\t')
    for row in reader:
	if len(row) >= 3 :
		text = row[0]
		x = float(row[1])
		y = float(row[2])
		drawing.add(dxf.point((x,y), color=7))
		drawing.add(dxf.text(text, insert=(x,y), color=3, height=100.0))
		i = 1+i
	else:
		print "len(row)=", len(row)
finally:
    file.close()
 
drawing.save()
print "Nb Points =",i
