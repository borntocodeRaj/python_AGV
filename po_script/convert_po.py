#!/usr/bin/env python
import os
import sys
import polib

import argparse

VERBOSE = False


def checkEmpty(var, message):
    if var is None:
        print message
        sys.exit(1)
    return False


def checkSource(aPath):
    if not os.path.isfile(aPath):
        print "The path %s do not exist" % (aPath)
        sys.exit(1)
    else:
        return True


def checkFormatFile(aPath, aFormat):
    if aPath.endswith(aFormat):
        return True
    else:
        return False


def checkcsvFile(aPath):
    return checkFormatFile(aPath, "csv")


def checkPoFile(aPath):
    return checkFormatFile(aPath, "po")


def getDicoFromPo(aFile, invertKey=False):
    po = polib.pofile(aFile)
    res = {}
    for entry in po:
        key = entry.msgid.replace("\n", "\\n").replace("\"", "\\\"")
        val = entry.msgstr.replace("\n", "\\n").replace("\"", "\\\"")
        if invertKey:
            res[val] = key
        else:
            res[key] = val
    return res


def convertPoTocsv(inputFile, outputFile, csvSep="\t"):
    po = polib.pofile(inputFile)
    inputDico = getDicoFromPo(inputFile)
    with open(outputFile, "w") as outputFd:
        for k in inputDico:
            csvLine = "\"%s\"%s\"%s\"" % (k, csvSep, inputDico[k])
            if VERBOSE:
                print csvLine
            outputFd.write(csvLine + "\n")


def cleanEndLine(line):
    if line.endswith('\n'):
        line = line[:-1]
    return line
    # TODO NEED TO BE FIX
    return line[:-2]


def cleanGuil(line):
    if len(line) > 0 and line[0] == "\"":
        line = line[1:]
    if len(line) > 0 and line[-1] == "\"":
        line = line[:-1]
    return line


def splitcsv(line, csvSep):
    return line.split(csvSep)


def getDicoFromcsv(inputFile, csvSep="\t"):
    sourceDico = {}
    with open(inputFile, "r") as inputFd:
        for line in inputFd:
            cl = cleanEndLine(line)
            res = splitcsv(cl, csvSep)
            if len(res) > 2:
                print "Error, can't split cvs line %s" % res
                sys.exit(1)

            key, value = res
            key = cleanGuil(key)
            value = cleanGuil(value)
            if VERBOSE:
                print "%s%s%s" % (key, csvSep, value)

            sourceDico[key] = value
    return sourceDico


def convertcsvToPo(inputFile, outputFile, csvSep="\t"):
    po = polib.POFile()
    po.metadata = {
        'Project-Id-Version': '1.0',
        'Report-Msgid-Bugs-To': 'you@example.com',
        'POT-Creation-Date': '2007-10-18 14:00+0100',
        'PO-Revision-Date': '2007-10-18 14:00+0100',
        'Last-Translator': 'you <you@example.com>',
        'Language-Team': 'English <yourteam@example.com>',
        'MIME-Version': '1.0',
        'Content-Type': 'text/plain; charset=utf-8',
        'Content-Transfer-Encoding': '8bit',
    }

    sourceDico = {}
    with open(inputFile, "r") as inputFd:
        for line in inputFd:
            occurrenceSourceFile = ""
            occurrenceSourceLine = ""
            occurrence = (occurrenceSourceFile, occurrenceSourceLine)
            cl = cleanEndLine(line)
            key, value = splitcsv(cl, csvSep)
            key = cleanGuil(key)
            value = cleanGuil(value)
            if VERBOSE:
                print "%s%s%s" % (key, csvSep, value)

            sourceDico[key] = value
            entry = polib.POEntry(
                msgid=key,
                msgstr=value,
                occurrences=[occurrence]
            )
            po.append(entry)
    po.save(outputFile)


def MergePoTocsv(inputFile, inputIbride, outputFile, csvSep="\t", defaultEncode="ISO-8859-1"):
    inputDico = getDicoFromPo(inputFile)
    ibrideDico = getDicoFromPo(inputIbride)

    with open(outputFile, "w") as outputFd:
        for k in inputDico:
            ibrideRes = ""
            if not k in ibrideDico:
                print "\"%s\" not presente in %s" % (k, inputIbride)
                # sys.exit(1)
            else:
                ibrideRes = ibrideDico[k]

            csvLine = "\"%s\"%s\"%s\"" % (inputDico[k], csvSep, ibrideRes)
            if VERBOSE:
                print csvLine
            outputFd.write(csvLine.encode(defaultEncode) + "\n")


def MergecsvToPo(inputFile, inputIbride, outputFile, csvSep="\t", defaultEncode="ISO-8859-1", anEmail='you@example.com', lang="da_DK"):
    inputDico = getDicoFromcsv(inputFile)
    ibrideDico = getDicoFromPo(inputIbride, invertKey=True)
    po = polib.POFile(encoding=defaultEncode)

    po.metadata = {
        'Project-Id-Version': '1.0',
        'Report-Msgid-Bugs-To': anEmail,
        'POT-Creation-Date': '2007-10-18 14:00+0100',
        'PO-Revision-Date': '2007-10-18 14:00+0100',
        'Last-Translator': 'you <%s>' % (anEmail),
        'Language-Team': 'English <%s>' % (anEmail),
        'Language': lang,
        'MIME-Version': '1.0',
        'Content-Type': 'text/plain; charset=%s' % (defaultEncode),
        'Content-Transfer-Encoding': '8bit',
    }

    with open(outputFile, "w") as outputFd:

        for k in inputDico:
            if not k in ibrideDico:
                print "\"%s\" not presente in %s" % (k, inputIbride)
                sys.exit(1)
            csvLine = "\"%s\"%s\"%s\"" % (
                ibrideDico[k].encode(defaultEncode), csvSep, inputDico[k])
            if VERBOSE:
                print csvLine
            occurrenceSourceFile = ""
            occurrenceSourceLine = ""
            occurrence = (occurrenceSourceFile, occurrenceSourceLine)
               
            msg_id = ibrideDico[k].decode(
                encoding=defaultEncode, errors='strict')
            msg_str = inputDico[k].decode(
                encoding=defaultEncode, errors='strict')
            # print msg_id    
            # print inputDico[k]
            # print msg_str
            if msg_str == "":
                print "WARNING: no Entry for key: \"%s\" Fix or use result at your own risk" % (k)
                msg_str = k

            entry = polib.POEntry(
                msgid=msg_id,
                msgstr=msg_str,
                occurrences=[occurrence]
            )
            po.append(entry)

    po.save(outputFile, repr_method='__unicode__')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--verbose", "-v", help="increase output verbosity", action="store_true")
    parser.add_argument(
        "--debug", "-d", help="output debug info", action="store_true")
    parser.add_argument(
        "--inputFile", "--if", "-i", help="path to the input file")
    parser.add_argument(
        "--inputIbride", "--bf", "-b", help="path to the ibride input file")
    parser.add_argument(
        "--outputFile", "-of", "-o", help="path to the output file")
    args = parser.parse_args()
    if args.verbose:
        VERBOSE = True
        print("verbosity turned on")
    else:
        pass
    checkEmpty(args.inputFile, "Error no inputfile")
    checkEmpty(args.outputFile, "Error no outputFile")
    checkSource(args.inputFile)

    if checkPoFile(args.inputFile):
        if checkcsvFile(args.outputFile):
            if args.inputIbride is not None and checkSource(args.inputIbride) and checkPoFile(args.inputIbride):
                MergePoTocsv(args.inputFile, args.inputIbride, args.outputFile)
            else:
                convertPoTocsv(args.inputFile, args.outputFile)
        else:
            print "output file is not a csv file"
        sys.exit(1)

    elif checkcsvFile(args.inputFile):
        if checkPoFile(args.outputFile):
            if args.inputIbride is not None and checkSource(args.inputIbride) and checkPoFile(args.inputIbride):
                MergecsvToPo(args.inputFile, args.inputIbride, args.outputFile)
            else:
                convertcsvToPo(args.inputFile, args.outputFile)
        else:
            print "output file is not a po file"
        sys.exit(1)

    else:
        print "Input is not a po file or csv"
        sys.exit(1)


if __name__ == "__main__":
    main()
