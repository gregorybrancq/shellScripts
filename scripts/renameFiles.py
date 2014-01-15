#!/usr/bin/env python

'''
rename files in a same directory
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

HEADER = "RENAME_FILE"
progName = re.sub(" ", "_", os.path.basename(sys.argv[0]))

t = str(datetime.datetime.today().isoformat("_"))
logFile = os.path.join(logDir, re.sub(" ", "_", progName) + "_" + t + ".log")

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

    dbg.info(HEADER, "In  main parsedArgs=" + str(parsedArgs))
    dbg.info(HEADER, "In  main args=" + str(args))

    for arg in args :
        arg.encode('latin1')
        dbg.info(HEADER, "In  main arg=" + str(arg))
        dbg.info(HEADER, "In  main cwd=" + str(os.getcwd()))
        if (os.path.isdir(arg)) :
            dirN = os.path.join(os.getcwd(), arg)
        else :
            dirN = os.getcwd()

    ## Launch the pyrenamer program
    cmdToLaunch='pyrenamer "' + str(dirN) + '"'
    dbg.info(HEADER, "In  main cmdToLaunch=" + str(cmdToLaunch))
    procPopen = subprocess.Popen(cmdToLaunch, shell=True, stderr=subprocess.STDOUT)
    procPopen.wait()

    dbg.info(HEADER, "Out main")



if __name__ == '__main__':
 
    ## Create log class
    dbg = LOGC(logFile, "unpack", parsedArgs.debug, parsedArgs.gui)

    main()

###############################################

