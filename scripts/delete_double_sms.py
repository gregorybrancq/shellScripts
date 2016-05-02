#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Concatene PDF files
'''



## Import
import sys
import os
import time, datetime
import subprocess
from optparse import OptionParser

## common
sys.path.append("../scripts")
from python_common import *
HEADER = "DEL_2_SMS"

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

parser.add_option(
    "-i",
    action  = "store",
    dest    = "inFile",
    default = "",
    help    = "input file"
    )

parser.add_option(
    "-o",
    action  = "store",
    dest    = "outFile",
    default = "sms_filter.xml",
    help    = "output file"
    )

(parsedArgs , args) = parser.parse_args()

###############################################



###############################################
## Global variables
###############################################

t = str(datetime.datetime.today().isoformat("_"))
logFile = os.path.join(logDir, HEADER + "_" + t + ".log")
errC = 0

###############################################





###############################################
###############################################
##                FUNCTIONS                  ##
###############################################
###############################################

def concatFile(fileList) :
    global dbg
    dbg.info(HEADER, "In  concatFile")

    dbg.info(HEADER, "Out concatFile")

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
    dbg.info(HEADER, "In  main")

    # Open input file
    try :
        fdi = open(parsedArgs.inFile, 'r')
    except (IOError, OSError) as e:
        dbg.exit(1, "Can't open file " + parsedArgs.inFile + "\n" + str(e), HEADER)

    # Read it
    msg = str()
    listD = list()
    for line in fdi.readlines() :

        if re.search("sms protocol.*date=.*",line) :
            dateP = re.findall('date="(.*)"', line)[0]
            if not listD.__contains__(dateP) :
                print "DBG 1 add dateP=" + str(dateP)
                msg += line
                listD.append(dateP)
            else :
                print "DBG 2 remove double line="+str(line)
        else :
            msg += line
        # Add line if needed

    # Write output file
    try :
        fdo = open(parsedArgs.outFile, 'w')
        fdo.write(msg)
        fdo.flush
        fdo.close()
    except (IOError, OSError) as e:
        log.exit(2, "Can't open file " + parsedArgs.outFile + "\n" + str(e), HEADER)



    dbg.info(HEADER, "Out main")

###############################################




if __name__ == '__main__':
 
    ## Create log class
    dbg = LOGC(logFile, HEADER, parsedArgs.debug, False)

    main()


