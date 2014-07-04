#!/usr/bin/env python
# -*-coding:Latin-1 -*

'''
Backup Money files
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
HEADER = "backupMoney"

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

t = str(datetime.datetime.today().isoformat("_"))
logFile = os.path.join(logDir, HEADER + "_" + t + ".log")
lockFile = os.path.join(logDir, HEADER + ".lock")
warnC = 0

fileOriginal = os.path.join(homeDir, "Informatique/Windows/Money/greg.mny")
fileBackupDir = os.path.join(homeDir, "Informatique/Windows/Money/Backup")
fileBackupList = []
fileBackupName = ""

###############################################




###############################################
###############################################
##                FUNCTIONS                  ##
###############################################
###############################################

def findBackupFiles() :
    global dbg
    global fileBackupList
    dbg.info(HEADER, "In  findBackupFiles")

    fileBackupList = [ f for f in os.listdir(fileBackupDir) if (os.path.isfile(os.path.join(fileBackupDir,f))) ]
    dbg.info(HEADER, "In  findBackupFiles fileList=" + str(fileBackupList))
    

    dbg.info(HEADER, "Out findBackupFiles")


def backupToDo() :
    global dbg
    global fileBackupName
    dbg.info(HEADER, "In  backupToDo")

    # find the last backup file name
    findBackupFiles()

    ## Look if it's necessary to backup
    findBackup = False
    for f in fileBackupList :
        dbg.info(HEADER, "In  compare fileBackup=" + str(f))
        comp = filecmp.cmp(fileOriginal, os.path.join(fileBackupDir, f))
        if comp :
            dbg.info(HEADER, "In  compare fileBackup find")
            fileBackupName = f
            findBackup = True

    if not findBackup :
        now = datetime.datetime.now()
        newName = "Backup-" + str(now.strftime("%Y-%m-%d") + ".mny")
        dbg.info(HEADER, "In  compare copy newName=" + str(newName))
        shutil.copy2(fileOriginal, os.path.join(fileBackupDir, newName))

    dbg.info(HEADER, "Out backupToDo")

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

    ## Backup file
    backupToDo()
    
    dbg.info(HEADER, "Out main")



if __name__ == '__main__':
 
    ## Create log class
    dbg = LOGC(logFile, HEADER, parsedArgs.debug, parsedArgs.gui)

    main()

###############################################

