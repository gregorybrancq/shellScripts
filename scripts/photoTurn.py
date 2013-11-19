#!/usr/bin/env python

'''
Turn images depends on the EXIF information
'''



## Import
import sys
import os
import os.path
from os.path import expanduser
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

## directory
home = expanduser("~")
if os.environ.get('DELL') :
    persoDir=os.path.join(home,"Perso/work/perso")
else :
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

HEADER = "PHOTO TURN"
progName = re.sub(" ", "_", os.path.basename(sys.argv[0]))

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

def exifConvert(photoList) :
    global dbg
    global warnC
    dbg.info(HEADER, "In  exifConvert")

    oldDir = os.getcwd()

    for (photoD, photoN, photoE) in photoList :
        dbg.info(HEADER, "In  exifConvert directory " + str(photoD) + "  convert " + photoN + photoE)

        if (photoD != "") :
            os.chdir(photoD)

        procPopen = subprocess.Popen('exifautotran "' + photoN + photoE + '"', shell=True, stderr=subprocess.STDOUT)
        procPopen.wait()
        if (procPopen.returncode != 0) :
            warnC += 1
            dbg.warn(HEADER, "In  exifConvert file " + str(os.path.join(photoD, photoN + photoE)) + " was not turned.")

        if (photoD != "") :
            os.chdir(oldDir)


    dbg.info(HEADER, "Out exifConvert")

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
    dbg.info(HEADER, "In  main")

    photoList = list()

    dbg.info(HEADER, "In  main parsedArgs=" + str(parsedArgs))
    dbg.info(HEADER, "In  main args=" + str(args))

    ## Create list of files
    extAuth=[".JPG", ".jpg", ".JPEG", ".jpeg"]
    (photoList, warnC) = listFromArgs(dbg, HEADER, args, extAuth)

    ## Verify if there is at least one photo to unpack
    if (len(photoList) == 0) :
        dialog_error("Pivoter les images", "\nNo photo has been found\n")
    else :
        dbg.info(HEADER, "In  main photo to convert = " + str(len(photoList)))

    ## Avoid another same program to run
    verify_lock_file(lockFile)
    create_lock_file(lockFile)

    ## Convert them
    exifConvert(photoList)
    msg = "\nJob fini : " + str(len(photoList)) + " images converties.\n\nLog file = "+ str(logFile)
    if (warnC != 0) :
        msg += "\nWarning = " + str(warnC)
    dialog_info("Pivoter les images", msg)
    
    ## Remove lock file
    remove_lock_file(lockFile)
    
    dbg.info(HEADER, "Out main")

###############################################




if __name__ == '__main__':
 
    ## Create log class
    dbg = LOGC(logFile, progName, parsedArgs.debug, parsedArgs.gui)

    main()


