#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Written by Gregory Brancq
# October 2018
# Public domain software

"""
Program to sort images files in corresponding directory
"""
  

## Import
import sys
import os
import re
import shutil
from datetime import datetime
from optparse import OptionParser

## common
from python_common import *
HEADER = "sortImag"

## directory
logDir = getLogDir()

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

parser.add_option(
    "-t",
    "--target",
    action  = "store",
    dest    = "target",
    default = None,
    help    = "Target directory to analyze"
    )


(parsedArgs , args) = parser.parse_args()

###############################################



###############################################
## Global variables
###############################################

t = str(datetime.today().isoformat("_"))
logFile = os.path.join(logDir, HEADER + "_" + t + ".log")
errC = 0

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
    log.info(HEADER, "In  main parsedArgs.target=" + str(parsedArgs.target))

    ## Create directory and move file
    extAuth=[".jpg", ".JPG", ".jpeg", ".JPEG", ".mp4", ".MP4"]
    for f in os.listdir(parsedArgs.target) :
        (fileN, extN) = os.path.splitext(f)
        if os.path.isfile(os.path.join(parsedArgs.target,f)) and extAuth.__contains__(extN) :
            log.dbg("file ok "+str(f))
            if re.search("20[0-9]{6}", fileN) :
                (year, month, day) = re.findall("(20[0-9]{2})([0-9]{2})([0-9]{2})", fileN)[0]
                dirN=year+"-"+month+"-"+day
                log.dbg("dirN="+str(dirN))
                if not os.path.isdir(dirN) :
                    log.dbg("Create directory "+dirN)
                    os.mkdir(dirN)
                log.dbg("Move "+f+" to "+dirN)
                shutil.move(f, dirN)

                    

    #(fileList, warnC) = listFromArgs(log, HEADER, parsedArgs.target, extAuth)

    log.info(HEADER, "Out main")

###############################################




if __name__ == '__main__':
 
    ## Create log class
    log = LOGC(logFile, HEADER, parsedArgs.debug)
    main()

