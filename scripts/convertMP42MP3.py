#!/usr/bin/env python
# -*- coding: latin1 -*-

'''
Convert MP4 to MP3
'''



## Import
import sys
import os
import os.path
from os.path import expanduser
import time, datetime
import subprocess
from optparse import OptionParser

# use for graphical interface
import gobject
import gtk
import pygtk
pygtk.require('2.0')
gtk.gdk.threads_init()

## directory
home = expanduser("~")
persoDir=os.path.join(home,"Greg/work/perso")
logDir=os.path.join(persoDir,"log")

## common
from python_common import *

###############################################



###############################################
###############################################
##              Line Parsing                 ##
###############################################
###############################################

parsedArgs = {}
parser = OptionParser()


parser.add_option(
    "--debug",
    action  = "store_true",
    dest    = "debug",
    default = False,
    help    = "Display all debug information"
    )

parser.add_option(
    "--nogui",
    action  = "store_false",
    dest    = "gui",
    default = True,
    help    = "Print information in a shell"
    )

(parsedArgs , args) = parser.parse_args()

###############################################



###############################################
## Global variables
###############################################

HEADER = "CONVMP42MP3"
progName = os.path.basename(sys.argv[0])

t = str(datetime.datetime.today().isoformat("_"))
logFile = os.path.join(logDir, re.sub(" ", "_", progName) + "_" + t + ".log")

errC = 0

###############################################





###############################################
###############################################
##                FUNCTIONS                  ##
###############################################
###############################################

def convertFile(fileList) :
    global dbg
    global errC
    dbg.info(HEADER, "In  convertFile")

    oldDir = os.getcwd()

    for (fileD, fileN, fileE) in fileList :
        dbg.info(HEADER, "In  convertFile directory " + str(fileD) + "  convertFile " + fileN + fileE)

        if (fileD != "") :
            os.chdir(fileD)

        cmd='pacpl --to mp3 -bitrate 320 "' + fileN + fileE + '"'
        dbg.info(HEADER, "In  convertFile cmd=" + str(cmd))
        procPopen = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT)
        procPopen.wait()
        if (procPopen.returncode != 0) :
            errC += 1
            dbg.error(HEADER, "In  convertFile file: issue with " + str(os.path.join(fileD, fileN + fileE)))

        if (fileD != "") :
            os.chdir(oldDir)

    dbg.info(HEADER, "Out convertFile")

###############################################






###############################################
###############################################
###############################################
##                 MAIN                      ##
###############################################
###############################################
###############################################


def main() :
    global dbg
    warnC = 0
    dbg.info(HEADER, "In  main")

    fileList = list()

    dbg.info(HEADER, "In  main parsedArgs=" + str(parsedArgs))
    dbg.info(HEADER, "In  main args=" + str(args))

    ## Create list of files
    extAuth=[".mp4", ".MP4"]
    (fileList, warnC) = listFromArgs(dbg, HEADER, args, extAuth)

    ## Verify if there is at least one photo to convertPdf2Jpg
    if (len(fileList) == 0) :
        dialog_error("Convert MP4 files", "\nNo video has been found\n")
    else :
        dbg.info(HEADER, "In  main videos to convert = " + str(len(fileList)))

    ## Convert them
    convertFile(fileList)

    msg = "\nJob fini : " + str(len(fileList)) + " video a convertir.\n"
    if (warnC != 0) :
        msg += "\nWarning = " + str(warnC)
    if (errC != 0) :
        msg += "\nError = " + str(errC)
    msg += "\n\nLog file = " + str(logFile)
    dialog_info("Convert video", msg)
    
    dbg.info(HEADER, "Out main")

###############################################




if __name__ == '__main__':
 
    ## Create log class
    dbg = LOGC(logFile, "convertMP42MP3", parsedArgs.debug, parsedArgs.gui)

    main()


