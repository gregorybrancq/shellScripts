#!/usr/bin/env python
# -*- coding: utf-8 -*-



## Import
import sys
import os, os.path
import re
import logging, logging.config
import time
from datetime import datetime, timedelta
import subprocess
from optparse import OptionParser

## common
from python_common import *
progName = "dodoJuju"

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
    help    = "Display all debug information."
    )

parser.add_option(
    "-b",
    "--block",
    action  = "store_true",
    dest    = "block",
    default = False,
    help    = "Block keyboard and mouse."
    )

parser.add_option(
    "-u",
    "--unblock",
    action  = "store_true",
    dest    = "unblock",
    default = False,
    help    = "Unblock keyboard and mouse."
    )

parser.add_option(
    "-e",
    "--enable",
    action  = "store_true",
    dest    = "enable",
    default = False,
    help    = "Block and unblock keyboard and mouse depending time part."
    )

parser.add_option(
    "-d",
    "--disable",
    action  = "store_true",
    dest    = "disable",
    default = False,
    help    = "Disable this program."
    )

(parsedArgs , args) = parser.parse_args()

###############################################




###############################################
## Global variables
###############################################

## directory
scriptDir = getScriptDir()
logDir  = getLogDir()

## logging
# load config
logging.config.fileConfig(os.path.join(scriptDir, 'logging.conf'))
# create logger
log = logging.getLogger(progName)

logFile = os.path.join(logDir, progName + "_" \
            + str(datetime.today().isoformat("_") + ".log"))

# false will suspend pc
userSlot = [
    ["lundi",    {"00:00": False, "06:00": True, "23:45": False}],
    ["mardi",    {"00:00": False, "06:00": True, "23:45": False}],
    ["mercredi", {"00:00": False, "06:00": True, "23:45": False}],
    ["jeudi",    {"00:00": False, "06:00": True, "23:45": False}],
    ["vendredi", {"00:00": False, "06:00": True}],
    ["samedi",   {"00:00": True,  "01:00": False, "07:00": True}],
    ["dimanche", {"00:00": True,  "01:00": False, "07:00": True, "23:45": False}]
]
###############################################




###############################################
###############################################
##                  CLASS                    ##
###############################################
###############################################

class Hardwares():
    def __init__(self) :
        self.hardwares = list()
 
    def __str__(self) :
        res = str()
        i=1
        for hardware in self.hardwares :
            res += "## Hardware " + str(i) + "\n"
            res += str(hardware) + "\n"
            i+=1
        return res

    def init(self, *hardwares) :
        for hardware in hardwares :
            hardwareC = Hardware(hardware[0], hardware[1])
            self.hardwares.append(hardwareC)

    def block(self) :
        log.info("In  block " + self.short)
        for hardware in hardwares :
            hardware.block()
        log.info("Out block")
    
    def unblock(self) :
        log.info("In  unblock " + self.short)
        for hardware in hardwares :
            hardware.unblock()
        log.info("Out unblock")


class Hardware():
    def __init__(self, name, fullName) :
        self.short = name
        self.full = fullName
        self.type = "pointer"
        self.getId()

    def __str__(self) :
        res = str()
        res += "#    name = " + str(self.short) + "\n"
        res += "#    full = " + str(self.full) + "\n"
        res += "#    id   = " + str(self.id)
        return res

    def getId(self) :
        try :
            self.id = subprocess.check_output(["xinput", "list", "--id-only", "pointer:" + str(self.full)]).strip()
        except subprocess.CalledProcessError :
            log.error("In getId : error with " + str(self.short))
    
    def block(self) :
        log.info("In  block " + self.short)
        #subprocess.call(["xinput", "disable", str(self.id)])
        log.info("Out block")
    
    def unblock(self) :
        log.info("In  unblock " + self.short)
        subprocess.call(["xinput", "enable", str(self.id)])
        log.info("Out unblock")


class EnableProg():
    def __init__(self) :
        self.enable = bool()
        self.disableFile = os.path.join("/tmp", progName + ".disable")
        self.checkDisableFile()

    def __str__(self) :
        res = str()
        res += "# disableFile = " + str(self.disableFile) + "\n"
        return res

    # if this program can be launched
    def isEn(self) :
        if self.enable :
            return True
        return False

    # Enable it
    def enProg(self) :
        log.info("In  enProg")
        if os.path.isfile(self.disableFile) :
            log.info("Delete disableFile " + str(self.disableFile))
            os.remove(self.disableFile)
        self.enable = True
    
    # Disable it
    def disProg(self) :
        log.info("In  disProg")
        fd = open(self.disableFile, 'w')
        fd.write(str(datetime.now()))
        fd.close()
        self.enable = False
        log.info("Out disProg")

    # Check file date creation is
    #  return True  if > 1 day
    #  return False if < 1 day
    def checkFileDate(self) :
        fd = open(self.disableFile, 'r')
        dateFileStr = fd.read().rstrip('\n')
        dateFileDT = datetime.strptime(dateFileStr, "%Y-%m-%d %H:%M:%S.%f")
        currentDT = datetime.now()
        if (dateFileDT + timedelta(days=1) < currentDT) :
            log.info("In  checkFileDate file has been created more than 1 day")
            return True
        return False

    # Check if disableFile exists more than one day
    def checkDisableFile(self) :
        if not os.path.isfile(self.disableFile) :
            log.info("In  checkDisableFile : no disableFile")
            self.enable = True
        else :
            # check if more than one day
            if self.checkFileDate() :
                log.info("In  checkDisableFile : more than one day")
                self.enProg()
            else :
                log.info("In  checkDisableFile : less than one day")
                self.enable = False



class TimeSlot():
    def __init__(self) :
        self.curDOW = datetime.now().weekday()
        self.curTime = time.strftime("%H:%M")

    def __str__(self) :
        res = str()
        res += "# current day of week = " + str(self.curDOW) + "\n"
        res += "# current time        = " + str(self.curTime) + "\n"
        return res

    # Check if datetime is in timeSlot defined by user
    def inTS(self) :
        log.info("In  inTS")
        for userTime in userSlot[self.curDOW][1] :
            print "GBR userTime=" + str(userTime)
            if self.curTime > userTime :
                return userSlot[self.curDOW][1][userTime]

    def suspend(self) :
        log.info("Suspend machine")
        #subprocess.call(["systemctl", "suspend", str(self.id)])

    def checkSuspend(self) :
        log.info("In  checkSuspend")
        if not self.inTS() :
            self.suspend()




###############################################






###############################################
###############################################
###############################################
##                 MAIN                      ##
###############################################
###############################################
###############################################

def main() :
    log.info("In  main")

    hardwares = Hardwares()
    hardwares.init(["Logitech", "TypeMatrix.com USB Keyboard"], ["mouseJuju", "MOSART Semi. 2.4G Wireless Mouse"])
    print str(hardwares)
    
    enProg = EnableProg()

    if parsedArgs.block :
        hardwares.block()
    elif parsedArgs.unblock :
        hardwares.unblock()
    elif parsedArgs.enable :
        enProg.enProg()
    elif parsedArgs.disable :
        enProg.disProg()
    else :
        if enProg.isEn() :
            ts = TimeSlot()
            print str(ts)
            ts.checkSuspend()
    
    log.info("Out main")



if __name__ == '__main__':
 
    main()

