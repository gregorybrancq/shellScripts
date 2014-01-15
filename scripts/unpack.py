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

# use for graphical interface
import gobject
import gtk
import pygtk
pygtk.require('2.0')
gtk.gdk.threads_init()

## common
from python_common import *

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

HEADER = "  UNPACK  "
progName = os.path.basename(sys.argv[0])

t = str(datetime.datetime.today().isoformat("_"))
logFile = os.path.join(logDir, re.sub(" ", "_", progName) + "_" + t + ".log")
lockFile = os.path.join(logDir, progName + ".lock")

warnC = 0

###############################################




###############################################
###############################################
##                FUNCTIONS                  ##
###############################################
###############################################


def unpack(movieList) :
    global dbg
    global warnC
    dbg.info(HEADER, "In  unpack")

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
        dbg.info(HEADER, "In  unpack directory " + str(movieD) + "  convert " + str(movieN) + str(movieE) + " to " + str(movieN) + " unpack" + str(movieE))

        if (movieD != "") :
            os.chdir(movieD)

        ## Run the job
        procPopen = subprocess.Popen('avidemux --force-unpack --load "' + movieN + movieE + '" --audio-map --save-unpacked-vop "' + movieN + " unpack" + movieE + '" --nogui --quit', shell=True, stderr=subprocess.STDOUT)
        procPopen.wait()
        if (procPopen.returncode != 0) :
            warnC += 1
            dbg.warn(HEADER, "In  unpack file " + str(os.path.join(movieD, movieN + movieE)) + " was not unpacked.")

        ## replace the original file
        if os.path.isfile(os.path.join(movieD, movieN + " unpack" + movieE)) :
            try :
                dbg.info(HEADER, "In  unpack move the original file " + os.path.join(movieD, movieN + movieE) + " to " + os.path.join(homeDir, "Vidéos/Original", movieN + movieE))
                os.rename(os.path.join(movieD, movieN + movieE), os.path.join(homeDir, "Vidéos/Original", movieN + movieE))
                dbg.info(HEADER, "In  unpack rename the unpack file " + os.path.join(movieD, movieN + " unpack" + movieE) + " to " + os.path.join(movieD, movieN + movieE))
                os.rename(os.path.join(movieD, movieN + " unpack" + movieE), os.path.join(movieD, movieN + movieE))
            except :
                dbg.info(HEADER, "In  unpack impossible to replace the original file. Directory=" + str(movieD) + "  Name=" + str(movieN) + "  Extension=" + str(movieE))

        if (movieD != "") :
            os.chdir(oldDir)

    dbg.info(HEADER, "Out unpack")

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
    global warnC
    movieList = list()
    dbg.info(HEADER, "In  main")

    dbg.info(HEADER, "In  main parsedArgs=" + str(parsedArgs))
    dbg.info(HEADER, "In  main args=" + str(args))

    ## Create list of files
    extAuth=[".avi", ".AVI"]
    (movieList, warnC) = listFromArgs(dbg, HEADER, args, extAuth)

    ## Verify if there is at least one movie to unpack
    if (len(movieList) == 0) :
        dbg.exit("1", "No movie has been found\n")

    ## Avoid another same program to run
    verify_lock_file(lockFile)
    create_lock_file(lockFile)

    ## Unpack them
    unpack(movieList)
    msg = "\nJob fini : " + str(len(movieList)) + " films convertis.\n\nLog file = "+ str(logFile)
    if (warnC != 0) :
        msg += "\nWarning = " + str(warnC)
    dialog_info(progName, msg)
    
    ## Remove lock file
    remove_lock_file(lockFile)
    
    dbg.info(HEADER, "Out main")



if __name__ == '__main__':
 
    ## Create log class
    dbg = LOGC(logFile, progName, parsedArgs.debug, parsedArgs.gui)

    main()

###############################################

