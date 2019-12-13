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
from datetime import datetime
import subprocess
from optparse import OptionParser

## common
from python_common import *
HEADER = "PdfTOKobo"

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
warnC = 0
errC = 0

###############################################




###############################################
###############################################
##                FUNCTIONS                  ##
###############################################
###############################################


def convert(pdfList) :
    global log
    global errC
    log.info(HEADER, "In  convert")

    oldDir = os.getcwd()

    for (pdfDir, pdfName, pdfExt) in pdfList :
        run = True
        log.info(HEADER, "In  convert directory '" + str(pdfDir) + "', convert '" + str(pdfName) + str(pdfExt) + "' to '" + str(pdfName) + "_k2pdfopt" + str(pdfExt) + "'")

        if (pdfDir != "") :
            os.chdir(pdfDir)

        ## Already converted ?
        if os.path.isfile(pdfName + " original" + pdfExt) or re.search(" original", pdfName) :
            run = False

        if run :

            ## Run the job
            cmdToLaunch='k2pdfopt -w 958 -h 1320 -dpi 213 -idpi -2 -x -ui- -m 0,0,0,0 -ocr t -ocrhmax 1.5 -ocrvis s "' + str(pdfName) + str(pdfExt) + '"'
            log.info(HEADER, "In  convert cmdToLaunch=" + str(cmdToLaunch))
            procPopen = subprocess.Popen(cmdToLaunch, shell=True, stderr=subprocess.STDOUT)
            procPopen.wait()
            if (procPopen.returncode != 0) :
                errC += 1
                log.error(HEADER, "In  convert, file " + str(os.path.join(pdfDir, pdfName + pdfExt)) + " was not successful.")

            ## replace the original file
            # if os.path.isfile(pdfName + "_k2opt" + pdfExt) :
            #     try :
            #         log.info(HEADER, "In  convert, move the original file " + pdfName + pdfExt + " to " + pdfName + " original" + pdfExt)
            #         os.rename(pdfName + pdfExt, pdfName + " original" + pdfExt)
            #         log.info(HEADER, "In  convert, rename the convert file " + pdfName + "_k2opt" + pdfExt + " to " + pdfName + pdfExt)
            #         os.rename(pdfName + "_k2opt" + pdfExt, pdfName + pdfExt)
            #     except :
            #         log.info(HEADER, "In  convert impossible to replace the original file. Directory=" + str(pdfDir) + "  Name=" + str(pdfName) + "  Extension=" + str(pdfExt))
            # else :
            #     log.info(HEADER, "In  convert, file " + os.path.join(pdfDir, pdfName + pdfExt) + " doesn't exist")

        else :
            log.info(HEADER, "In  convert, file " + os.path.join(pdfDir, pdfName + pdfExt) + " already converted")

        if (pdfDir != "") :
            os.chdir(oldDir)

    log.info(HEADER, "Out convert")

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
    pdfList = list()
    log.info(HEADER, "In  main")

    log.info(HEADER, "In  main parsedArgs=" + str(parsedArgs))
    log.info(HEADER, "In  main args=" + str(args))

    ## Create list of files
    extAuth=[".pdf", ".PDF"]
    (pdfList, warnC) = listFromArgs(log, HEADER, args, extAuth)

    ## Verify if there is at least one file to convert
    if (len(pdfList) == 0) :
        log.exit("1", "No pdf file has been found\n")

    ## Convert them
    log.info(HEADER, "Script will convert " + str(len(pdfList)) + " file(s)")
    convert(pdfList)

    ## End dialog
    MessageDialogEnd(warnC, errC, logFile, "Convert Kobo", "\nJob fini : " + str(len(pdfList)) + " livres convertis.\nLivre : " + str(pdfList) + ".")
    
    log.info(HEADER, "Out main")



if __name__ == '__main__':
 
    ## Create log class
    log = LOGC(logFile, HEADER, parsedArgs.debug)

    main()

###############################################

