#!/usr/bin/env python
# -*-coding:Latin-1 -*

'''
Unpack video films
'''



## Import
import sys
import os
import re
import time, datetime
import subprocess
from optparse import OptionParser

## common
from python_common import *
HEADER = "Unpack"

## directory
homeDir = getHomeDir()
logDir  = getLogDir()

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

t = str(datetime.datetime.today().isoformat("_"))
logFile = os.path.join(logDir, HEADER + "_" + t + ".log")
lockFile = os.path.join(logDir, HEADER + ".lock")
warnC = 0

###############################################




###############################################
###############################################
##                FUNCTIONS                  ##
###############################################
###############################################


def unpack(movieList) :
    global log
    global warnC
    log.info(HEADER, "In  unpack")

    oldDir = os.getcwd()

    #movietoConvert = str()
    #if (len(movieList) > 1) :
    #    title = "Convert these files?"
    #else :
    #    title = "Convert this file?"
    #for (movieD, movieN, movieE) in movieList :
    #    movietoConvert += os.path.join(movieD, movieN + movieE) + "\n"
    #question = dialog_ask(title, movietoConvert)

    #if question :
    for (movieD, movieN, movieE) in movieList :
        log.info(HEADER, "In  unpack directory " + str(movieD) + "  convert " + str(movieN) + str(movieE) + " to " + str(movieN) + " unpack" + str(movieE))

        if (movieD != "") :
            os.chdir(movieD)

        ## Run the job
        procPopen = subprocess.Popen('avidemux --force-unpack --load "' + movieN + movieE + '" --audio-map --save-unpacked-vop "' + movieN + " unpack" + movieE + '" --nogui --quit', shell=True, stderr=subprocess.STDOUT)
        procPopen.wait()
        if (procPopen.returncode != 0) :
            warnC += 1
            log.warn(HEADER, "In  unpack file " + str(os.path.join(movieD, movieN + movieE)) + " was not unpacked.")

        ## replace the original file
        if os.path.isfile(os.path.join(movieD, movieN + " unpack" + movieE)) :
            try :
                log.info(HEADER, "In  unpack move the original file " + os.path.join(movieD, movieN + movieE) + " to " + os.path.join(homeDir, "Vidéos/Original", movieN + movieE))
                os.rename(os.path.join(movieD, movieN + movieE), os.path.join(homeDir, "Vidéos/Original", movieN + movieE))
                log.info(HEADER, "In  unpack rename the unpack file " + os.path.join(movieD, movieN + " unpack" + movieE) + " to " + os.path.join(movieD, movieN + movieE))
                os.rename(os.path.join(movieD, movieN + " unpack" + movieE), os.path.join(movieD, movieN + movieE))
            except :
                log.info(HEADER, "In  unpack impossible to replace the original file. Directory=" + str(movieD) + "  Name=" + str(movieN) + "  Extension=" + str(movieE))

        if (movieD != "") :
            os.chdir(oldDir)

    log.info(HEADER, "Out unpack")

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
    global warnC
    movieList = list()
    log.info(HEADER, "In  main")

    log.info(HEADER, "In  main parsedArgs=" + str(parsedArgs))
    log.info(HEADER, "In  main args=" + str(args))

    ## Create list of files
    extAuth=[".avi", ".AVI"]
    (movieList, warnC) = listFromArgs(log, HEADER, args, extAuth)

    ## Verify if there is at least one movie to unpack
    if (len(movieList) == 0) :
        log.exit("1", "No movie has been found\n")

    ## Avoid another same program to run
    verify_lock_file(lockFile)
    create_lock_file(lockFile)

    ## Unpack them
    unpack(movieList)

    ## End dialog
    dialog_end(warnC, errC, logFile, "Unpack movies", "\nJob fini : " + str(len(movieList)) + " films convertis.")
    
    ## Remove lock file
    remove_lock_file(lockFile)
    
    log.info(HEADER, "Out main")



if __name__ == '__main__':
 
    ## Create log class
    log = LOGC(logFile, HEADER, parsedArgs.debug)

    main()

###############################################

