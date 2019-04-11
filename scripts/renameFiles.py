#!/usr/bin/env python

'''
rename files in a same directory
'''



## Import
import sys
import os
import re
from datetime import datetime
import subprocess
from optparse import OptionParser

## common
from python_common import *
HEADER = "Rename_File"

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
    log.info(HEADER, "In  main")

    log.info(HEADER, "In  main parsedArgs=" + str(parsedArgs))
    log.info(HEADER, "In  main args=" + str(args))

    for arg in args :
        log.info(HEADER, "In  main arg=" + str(arg))
        log.info(HEADER, "In  main cwd=" + str(os.getcwd()))
        if (os.path.isdir(arg)) :
            dirN = os.path.join(os.getcwd(), arg)
        else :
            dirN = os.getcwd()
        break

    ## Launch the pyrenamer program
    cmdToLaunch='pyrenamer "' + str(dirN) + '"'
    log.info(HEADER, "In  main cmdToLaunch=" + str(cmdToLaunch))
    procPopen = subprocess.Popen(cmdToLaunch, shell=True, stderr=subprocess.STDOUT)
    procPopen.wait()

    log.info(HEADER, "Out main")



if __name__ == '__main__':
 
    ## Create log class
    log = LOGC(logFile, HEADER, parsedArgs.debug)

    main()

###############################################

