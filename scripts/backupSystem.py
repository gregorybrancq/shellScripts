#!/usr/bin/env python
# -*-coding:Latin-1 -*

'''
Backup System files

    - grub (in /boot/)
    - /etc
    - /opt
    - /usr
    - /var
    - home configuration files

'''



## Import
import sys
import os, os.path
import re
import time, datetime
from time import gmtime, strftime
import shutil
import glob
from optparse import OptionParser

## common
from python_common import *
HEADER = "backupSystem"

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

dirBackupList = ["/boot/grub", "/etc", "/opt", "/usr", "/var"]

backupDirName = strftime("%Y_%m_%d", gmtime())
backupBaseDir = "/mnt/backup/Backup/System"
backupDir = os.path.join(backupBaseDir, backupDirName)


###############################################




###############################################
###############################################
##                FUNCTIONS                  ##
###############################################
###############################################

def createDir(dirName) :
    if os.path.exists(dirName) :
        shutil.rmtree(dirName)
    os.makedirs(dirName)
    dbg.info(HEADER, "CreateDir created dir=" + dirName)


def copyDir(src, dest) :
    dbg.info(HEADER, "CopyDir src=" + src + ", dest=" + dest)
    try :
        shutil.copytree(src, dest, symlinks=True)
    except shutil.Error as e :
        dbg.warn(HEADER, "CopyDir copytree\n" + str(e))


def copyFile(src, dest) :
    dbg.info(HEADER, "CopyFile src=" + src + ", dest=" + dest)
    try :
        shutil.copy(src, dest)
    except shutil.Error as e :
        dbg.warn(HEADER, "CopyFile copy\n" + str(e))



def backupToDo() :
    global dbg
    global fileBackupName
    dbg.info(HEADER, "In  backupToDo")

    # create backup directory
    createDir(backupDir)

    # copy directories
    for dirToCopy in dirBackupList :
        backupDest = backupDir + dirToCopy
        copyDir(dirToCopy, backupDest)
            
    # copy home configuration files
    backupHomeDir = os.path.join(backupDir, "home_greg")
    createDir(backupHomeDir)
    listHomeCfg = glob.glob(os.path.join(homeDir, '.*'))
    for homeCfg in listHomeCfg :
        backupDest = backupHomeDir + re.sub(homeDir, "", homeCfg)
        if os.path.isdir(homeCfg) :
            copyDir(homeCfg, backupDest)
        else :
            copyFile(homeCfg, backupDest)

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
    dbg.info(HEADER, "In  main")

    ## Backup file
    backupToDo()
    
    dbg.info(HEADER, "Out main")



if __name__ == '__main__':
 
    ## Create log class
    dbg = LOGC(logFile, HEADER, parsedArgs.debug, parsedArgs.gui)

    main()

###############################################

