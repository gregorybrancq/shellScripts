#!/usr/bin/env python

'''
Convert PDF files into Kobo format
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

## common
from python_common import *
HEADER = "Pdf->Kobo"

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

t = str(datetime.datetime.today().isoformat("_"))
logFile = os.path.join(logDir, HEADER + "_" + t + ".log")
warnC = 0

###############################################




###############################################
###############################################
##                FUNCTIONS                  ##
###############################################
###############################################


def convert(pdfList) :
    global dbg
    global warnC
    dbg.info(HEADER, "In  convert")

    oldDir = os.getcwd()

    for (pdfDir, pdfName, pdfExt) in pdfList :
        run = True
        dbg.info(HEADER, "In  convert directory '" + str(pdfDir) + "', convert '" + str(pdfName) + str(pdfExt) + "' to '" + str(pdfName) + "_k2pdfopt" + str(pdfExt) + "'")

        if (pdfDir != "") :
            os.chdir(pdfDir)

        ## Already converted ?
        if os.path.isfile(pdfName + " original" + pdfExt) or re.search(" original", pdfName) :
            run = False

        if run :

            ## Run the job
            cmdToLaunch='k2pdfopt -w 958 -h 1320 -dpi 213 -idpi -2 -x -ui- -m 0,0,0,0 -ocr t -ocrhmax 1.5 -ocrvis s "' + str(pdfName) + str(pdfExt) + '"'
            dbg.info(HEADER, "In  convert cmdToLaunch=" + str(cmdToLaunch))
            procPopen = subprocess.Popen(cmdToLaunch, shell=True, stderr=subprocess.STDOUT)
            procPopen.wait()
            if (procPopen.returncode != 0) :
                warnC += 1
                dbg.warn(HEADER, "In  convert, file " + str(os.path.join(pdfDir, pdfName + pdfExt)) + " was not successful.")

            ## replace the original file
            # if os.path.isfile(pdfName + "_k2opt" + pdfExt) :
            #     try :
            #         dbg.info(HEADER, "In  convert, move the original file " + pdfName + pdfExt + " to " + pdfName + " original" + pdfExt)
            #         os.rename(pdfName + pdfExt, pdfName + " original" + pdfExt)
            #         dbg.info(HEADER, "In  convert, rename the convert file " + pdfName + "_k2opt" + pdfExt + " to " + pdfName + pdfExt)
            #         os.rename(pdfName + "_k2opt" + pdfExt, pdfName + pdfExt)
            #     except :
            #         dbg.info(HEADER, "In  convert impossible to replace the original file. Directory=" + str(pdfDir) + "  Name=" + str(pdfName) + "  Extension=" + str(pdfExt))
            # else :
            #     dbg.info(HEADER, "In  convert, file " + os.path.join(pdfDir, pdfName + pdfExt) + " doesn't exist")

        else :
            dbg.info(HEADER, "In  convert, file " + os.path.join(pdfDir, pdfName + pdfExt) + " already converted")

        if (pdfDir != "") :
            os.chdir(oldDir)

    dbg.info(HEADER, "Out convert")

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
    pdfList = list()
    dbg.info(HEADER, "In  main")

    dbg.info(HEADER, "In  main parsedArgs=" + str(parsedArgs))
    dbg.info(HEADER, "In  main args=" + str(args))

    ## Create list of files
    extAuth=[".pdf", ".PDF"]
    (pdfList, warnC) = listFromArgs(dbg, HEADER, args, extAuth)

    ## Verify if there is at least one file to convert
    if (len(pdfList) == 0) :
        dbg.exit("1", "No pdf file has been found\n")

    ## Convert them
    dbg.info(HEADER, "Script will convert " + str(len(pdfList)) + " file(s)")
    convert(pdfList)
    msg = "\nJob fini : " + str(len(pdfList)) + " livres convertis.\nLivre : " + str(pdfList) + "\n\nLog file = "+ str(logFile)
    if (warnC != 0) :
        msg += "\nWarning = " + str(warnC)
    dialog_info(progName, msg)
    
    dbg.info(HEADER, "Out main")



if __name__ == '__main__':
 
    ## Create log class
    dbg = LOGC(logFile, HEADER, parsedArgs.debug, parsedArgs.gui)

    main()

###############################################

