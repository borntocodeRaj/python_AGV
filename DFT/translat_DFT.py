#!/usr/bin/env python
# coding: UTF8 
import os
import sys
import polib

defaultEncode="UTF8"

import argparse

def checkEmpty(var, message):
    if var is None:
        print message
        sys.exit(1)
    return False

def splitDFT(inputDFT):
    res=[]
    with open(inputDFT, "r") as inputDFTFd:
        for line in inputDFTFd:
            res.append(line.split("\t"))
        
    return res

def writeDFT(listDFT,outputFile):
    with open(outputFile, "w") as outputDFTFd:
        for line in listDFT:
            lineResult=("\t".join(line))
            outputDFTFd.write(lineResult)

def getDicoFromPo(aFile):
    po = polib.pofile(aFile)
    res = {}
    for entry in po:
        key = entry.msgid.encode(defaultEncode)
        val = entry.msgstr.encode(defaultEncode)
        res[val] = key
    return res

def CleanErrorMessage(message):
    cleanMessage=message.replace("[","").replace("]","").split()
    return cleanMessage[1]

def getDicoFromBaDysf(aFile):
    res={}
    with open(aFile, "r") as aFiled:
        for line in aFiled:
            tmp=line.split("\t")
            if len(tmp)>3:
                res[tmp[0].replace("\"","")]=tmp[2]
    return res

def translatDFT(inputDFT, inputDico, outputFile):
    listDFT = splitDFT(inputDFT)
    dicoTranslate = getDicoFromBaDysf(inputDico)
    
    result=[]
    
    for line in listDFT:
        if len(line)>=5:
            toTrad = line[5]
            if CleanErrorMessage(line[4]) in dicoTranslate:
                toTrad = (dicoTranslate[CleanErrorMessage(line[4])])
                
            line[5]=toTrad
        result.append(line)
            
    writeDFT(result, outputFile)

def main():
    #ex:./translat_DFT.py -i test/DFT042016.log -b test/ba-dysf_0 -o DFT042016_fr.log

    parser = argparse.ArgumentParser(description='Translate DYSF file')
    parser.add_argument(
        "--verbose", "-v", help="increase output verbosity", action="store_true")
    parser.add_argument(
        "--debug", "-d", help="output debug info", action="store_true")
    parser.add_argument(
        "--inputFile", "--if", "-i", help="path to the input file ex: DFT042016.log")
    parser.add_argument(
        "--inputBaDysf", "--df", "-b", help="path to the Ba-dysf input file ex: ba-dysf_0")
    parser.add_argument(
        "--outputFile", "-of", "-o", help="path to the output file")
    args = parser.parse_args()
    if args.verbose:
        VERBOSE = True
        print("verbosity turned on")
    else:
        pass
        
    if (args.inputFile is None or
        args.inputBaDysf is None or
        args.outputFile is None):
        parser.print_help()
    
    checkEmpty(args.inputFile, "Error no inputfile")
    checkEmpty(args.inputBaDysf, "Error no inputBaDysf")
    checkEmpty(args.outputFile, "Error no outputfile")

    

    translatDFT(args.inputFile,args.inputBaDysf,args.outputFile)



if __name__ == "__main__":
    main()
