#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Split flac file into several thanks to cue file
'''



## Import
import sys
import os
from datetime import datetime
import subprocess
from optparse import OptionParser

## common
from python_common import *
HEADER = "SpliFlac"

## directory
logDir   = getLogDir()

###############################################



###############################################
###############################################
##              Line Parsing                 ##
###############################################
###############################################

parsedArgs = {}
parser = OptionParser()


parser.add_option(
    "-d",
    "--debug",
    action  = "store_true",
    dest    = "debug",
    default = False,
    help    = "Display all debug information"
    )

(parsedArgs , args) = parser.parse_args()

###############################################



###############################################
## Global variables
###############################################

t = str(datetime.today().isoformat("_"))
logFile = os.path.join(logDir, HEADER + "_" + t + ".log")
errC = 0
fileFlac = str()

###############################################





###############################################
###############################################
##                FUNCTIONS                  ##
###############################################
###############################################

def splitFlac(fileList) :
    global log
    global errC
    global fileFlac
    log.info(HEADER, "In  splitFlac")

    oldDir = os.getcwd()

    (file1D, file1N, file1E) = fileList[0]
    (file2D, file2N, file2E) = fileList[1]
    log.info(HEADER, "In  splitFlac file1=" + os.path.join(file1D, file1N + file1E))
    log.info(HEADER, "In  splitFlac file2=" + os.path.join(file2D, file2N + file2E))

    if ( (file1E == ".cue") or (file1E == ".CUE") ) and ((file2E == ".flac") or (file2E == ".FLAC") ) :
        fileCueD = file1D
        fileCueN = file1N
        fileCueE = file1E
        fileFlacD = file2D
        fileFlacN = file2N
        fileFlacE = file2E
    elif ( (file2E == ".cue") or (file2E == ".CUE") ) and ((file1E == ".flac") or (file1E == ".FLAC") ) :
        fileCueD = file2D
        fileCueN = file2N
        fileCueE = file2E
        fileFlacD = file1D
        fileFlacN = file1N
        fileFlacE = file1E
    else :
        MessageDialog(type_='error', title="Split Flac with Cue", message="\nThe 2 files must be flac AND cue.\n").run()

    log.info(HEADER, "In  splitFlac fileCue=" + os.path.join(fileCueD, fileCueN + fileCueE))
    log.info(HEADER, "In  splitFlac fileFlac=" + os.path.join(fileFlacD, fileFlacN + fileFlacE))
    fileFlac = os.path.join(fileFlacD, fileFlacN + fileFlacE)

    if (fileFlacD != fileCueD) :
        MessageDialog(type_='error', title="Split Flac with Cue", message="\nThe 2 files flac and cue must be in the same directory.\n").run()

    if (fileFlacD != "") :
        os.chdir(fileFlacD)

    cmd='shntool split -t "%p - %a - %n - %t" -f "' + fileCueN + fileCueE + '" -o flac "' + fileFlacN + fileFlacE + '"'
    log.info(HEADER, "In  splitFlac cmd=" + str(cmd))
    procPopen = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT)
    log.info(HEADER, "In  splitFlac before wait")
    procPopen.wait()
    log.info(HEADER, "In  splitFlac after wait returnCode = " + str(procPopen.returncode))
    if (procPopen.returncode != 0) :
        errC += 1
        log.error(HEADER, "In  splitFlac file: issue with " + str(os.path.join(fileFlacD, fileFlacN + fileFlacE)))

    log.info(HEADER, "In  splitFlac after check")
    if (fileFlacD != "") :
        os.chdir(oldDir)

    log.info(HEADER, "Out splitFlac")

###############################################






###############################################
###############################################
###############################################
##                 MAIN                      ##
###############################################
###############################################
###############################################


def main() :
    global log
    warnC = 0
    log.info(HEADER, "In  main")

    fileList = list()

    log.info(HEADER, "In  main parsedArgs=" + str(parsedArgs))
    log.info(HEADER, "In  main args=" + str(args))

    ## Create list of files
    extAuth=[".flac", ".FLAC", ".cue", ".CUE"]
    (fileList, warnC) = listFromArgs(log, HEADER, args, extAuth)

    ## Verify if there is at least one file to convert
    if (len(fileList) == 0) :
        MessageDialog(type_='error', title="Split Flac with Cue", message="\nNo flac and cue file have been found\n").run()
    elif (len(fileList) != 2) :
        MessageDialog(type_='error', title="Split Flac with Cue", message="\nOnly 2 files are allowed = flac and cue\n").run()

    log.info(HEADER, "In  main filelist = " + str(len(fileList)))

    ## Split it
    splitFlac(fileList)

    ## End dialog
    MessageDialogEnd(warnC, errC, logFile, "Convert music files", "\nJob fini : " + str(fileFlac) + " splitted.")
    
    log.info(HEADER, "Out main")

###############################################




if __name__ == '__main__':
 
    ## Create log class
    log = LOGC(logFile, HEADER, parsedArgs.debug)

    main()


