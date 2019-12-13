#!/usr/bin/env python
# -*-coding:Latin-1 -*

'''
Backup System files

    - grub (in /boot/)
    - /etc
    - /opt
    - /usr
    - /run
    - /var
    - home configuration files

'''



## Import
import sys
import os, os.path
import re
from datetime import datetime
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

(parsedArgs , args) = parser.parse_args()

###############################################




###############################################
## Global variables
###############################################

t = str(datetime.today().isoformat("_"))
logFile = os.path.join(logDir, HEADER + "_" + t + ".log")
lockFile = os.path.join(logDir, HEADER + ".lock")

dirBackupList = ["/boot/grub", "/etc", "/opt", "/usr", "/run", "/var"]

# variable to ignore pattern during copying for home
nameIgnoreList = list()
nameIgnoreList.append("/home/greg/.cache")
nameIgnoreList.append("/home/greg/.thunderbird")

backupDirName = strftime("%Y_%m_%d", gmtime())
#backupDirName = "2017_04_20"
backupBaseDir = "/home/greg/Backup/System"
backupDir = os.path.join(backupBaseDir, backupDirName)


###############################################




###############################################
###############################################
##                FUNCTIONS                  ##
###############################################
###############################################

def createDir(dirName) :
    global log
    if os.path.exists(dirName) :
        shutil.rmtree(dirName)
    os.makedirs(dirName)
    log.info(HEADER, "CreateDir created dir=" + dirName)


def copyDir(src, dest) :
    global log
    log.info(HEADER, "CopyDir src=" + src + ", dest=" + dest)
    try :
        if re.search("/var", src) :
            patterns = shutil.ignore_patterns("urandom", "cache", "postfix")
            shutil.copytree(src, dest, symlinks=True, ignore=patterns)
        else :
            shutil.copytree(src, dest, symlinks=True)
    except shutil.Error as e :
        log.warn(HEADER, "CopyDir copytree\n" + str(e))


def copyFile(src, dest) :
    global log
    log.info(HEADER, "CopyFile src=" + src + ", dest=" + dest)
    try :
        shutil.copy(src, dest)
    except shutil.Error as e :
        log.warn(HEADER, "CopyFile copy\n" + str(e))



def backupToDo() :
    global log
    global fileBackupName
    log.info(HEADER, "In  backupToDo")

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
        if not nameIgnoreList.__contains__(homeCfg) :
            backupDest = backupHomeDir + re.sub(homeDir, "", homeCfg)
            if os.path.isdir(homeCfg) :
                copyDir(homeCfg, backupDest)
            else :
                copyFile(homeCfg, backupDest)

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

    ## Backup file
    backupToDo()
    
    log.info(HEADER, "Out main")



if __name__ == '__main__':
 
    ## Create log class
    log = LOGC(logFile, HEADER, parsedArgs.debug)

    main()

###############################################

