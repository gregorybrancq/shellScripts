#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Send file(s) to DL FREE from nemo
'''



## Import
import sys
import os
import re
import time, datetime
from subprocess import Popen, PIPE
from optparse import OptionParser

## common
from python_common import *
HEADER = "FTP_FREE"

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

t = str(datetime.datetime.today().isoformat("_"))
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

    if args.__len__() != 1 :
        dialog_error("Send File to DL Free", "Only 1 file supported")
        sys.exit(-1)

    fileN = ""
    if (os.path.isfile(args[0])) :
        fileN = args[0]
    else :
        dialog_error("Send File to DL Free", args[0] + " is not a file")
        sys.exit(-1)

    ## Launch the ftp free program
    out = ""
    err = ""
    cmdToLaunch=getBinDir() + '/ftp-free "' + str(fileN) + '"'
    log.info(HEADER, "In  main cmdToLaunch=" + str(cmdToLaunch))
    procPopen = Popen(cmdToLaunch, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = procPopen.communicate()
    log.info(HEADER, "In  main result out\n" + str(out))
    log.info(HEADER, "In  main result err\n" + str(err))

    ## Print result
    msg = "Fichier envoyé : " + str(fileN) + "\n\n"
    if re.search("Fichier d'origine :", out) :
        msg += "URL de download: " + "\n"
        msg += "    " + re.findall("URL Fichier depose : (.*)", out)[0] + "\n"
    if re.search("URL pour suppression du fichier :", out) :
        msg += "URL de suppression: " + "\n"
        msg += "    " + re.findall("URL pour suppression du fichier : (.*)", out)[0] + "\n"
    
    if (err != "") :
        dialog_error("Send File to DL Free", msg)
    else :
        dialog_info("Send File to DL Free", msg)

    ## Send email
    log.info(HEADER, "In  main send mail")
    log.info(HEADER, "In  main send mail args[0]=" + str(args[0]))
    log.info(HEADER, "In  main send mail msg=" + str(msg))
    try:
        sendMail("Greg <gregory.brancq@free.fr>", "gregory.brancq@free.fr", "", "Send to DL Free : " + str(args[0]), str(msg), "");
    except :
        log.error(HEADER, "In  main send mail issue ")

    log.info(HEADER, "Out main")



if __name__ == '__main__':
 
    ## Create log class
    log = LOGC(logFile, HEADER, parsedArgs.debug)

    main()

###############################################

