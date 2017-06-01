#!/usr/bin/env python
# -*-coding:Latin-1 -*

'''
Backup Pondus files
'''



## Import
import sys
import os, os.path
import re
import time, datetime
import filecmp
import shutil
from optparse import OptionParser

## common
from python_common import *
HEADER = "backupPondus"

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

fileBackupDir = "/home/greg/Backup/Pondus"
fileBackupList = []
fileBackupName = ""

dirOriginal = os.path.join(homeDir, ".pondus")
files = os.listdir(dirOriginal)

###############################################




###############################################
###############################################
##                FUNCTIONS                  ##
###############################################
###############################################

def findBackupFiles() :
    global log
    global fileBackupList
    log.info(HEADER, "In  findBackupFiles")
    fileBackupList = [ f for f in os.listdir(fileBackupDir) if (os.path.isfile(os.path.join(fileBackupDir,f))) ]
    log.info(HEADER, "Out findBackupFiles fileList=" + str(fileBackupList))


def backupToDo(fileName) :
    global log
    global fileBackupName
    log.info(HEADER, "In  backupToDo " + str(fileName))

    ## Look if it's necessary to backup
    didBackup = False
    for f in fileBackupList :
        log.info(HEADER, "In  backupToDo fileBackup=" + str(f))
        comp = filecmp.cmp(os.path.join(dirOriginal, fileName), os.path.join(fileBackupDir, f))
        if comp :
            log.info(HEADER, "In  backupToDo fileBackup find")
            didBackup = True
            break

    if not didBackup :
        now = datetime.datetime.now()
        (fileN, extN) = os.path.splitext(fileName)
        newName = fileN + "_" + str(now.strftime("%Y-%m-%d") + extN)
        log.info(HEADER, "In  backupToDo copy newName=" + str(newName))
        shutil.copy2(os.path.join(dirOriginal, fileName), os.path.join(fileBackupDir, newName))

    log.info(HEADER, "Out backupToDo")

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

    # find backup file
    findBackupFiles()

    ## Backup file
    for f in files :
        backupToDo(f)
    
    log.info(HEADER, "Out main")



if __name__ == '__main__':
 
    ## Create log class
    log = LOGC(logFile, HEADER, parsedArgs.debug)

    main()

###############################################

