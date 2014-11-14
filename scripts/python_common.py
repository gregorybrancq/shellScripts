#!/usr/bin/env python
# -*- coding: latin1 -*-

'''
Common functions
'''

import os
from os.path import expanduser
import sys
import re
import pwd
import time
import datetime
import random

# use for graphical interface
import gobject
import gtk
import pygtk
pygtk.require('2.0')
gtk.gdk.threads_init()




###############################################
###############################################
##                CLASS LOG                  ##
###############################################
###############################################

class LOGC(object):
    def __init__(self, file_name, prog_name, debug, gui):
        self.fileName = file_name
        self.progName = prog_name
        self.dbg = debug
        self.gui = gui

    def writeLog(self, msg):
        if self.dbg :
            print " DBG " + self.progName + " : " + str(msg)
        
        msg += "\n"
        try :
            f = open(self.fileName, 'a+')
            f.write(msg)
            f.close()
        except IOError, OSError:
            pass

    def debug(self, msg):
        mes = " [ debug ] " + str(datetime.datetime.today().isoformat("_")) + " == " + msg
        if self.dbg :
            print " DBG " + self.progName + " : " + str(mes)
    def info(self, item, msg):
        mes = item + " [ info  ] " + str(datetime.datetime.today().isoformat("_")) + " == " + msg
        self.writeLog(mes)
    def warn(self, item, msg):
        mes = item + " [warning] " + str(datetime.datetime.today().isoformat("_")) + " == " + msg
        self.writeLog(mes)
    def error(self, item, msg):
        mes = item + " [ error ] " + str(datetime.datetime.today().isoformat("_")) + " == " + msg
        self.writeLog(mes)
        print "  ERROR " + self.progName + " :   Code " + str(item) + "\n" + str(msg) + "\n"
    def exit(self, item, msg):
        self.dbg = False
        if self.gui :
            mes = "ERROR " + self.progName + " :   Exit code " + str(item) + "\n" + str(msg) + "\n"
            dialog_error("ERROR " + self.progName + " code " + str(item), msg)
        else :
            mes = "  ERROR " + self.progName + " :   Exit code " + str(item) + "\n" + color_error + str(msg) + color_reset + "\n"
        self.writeLog(mes)
        sys.exit(color_error + mes + color_reset)




###############################################
###############################################
##                  GUI                      ##
###############################################
###############################################

## Dialog GUI
def dialog_info(title,msg) :
    dialog = gtk.MessageDialog(None,
        gtk.DIALOG_MODAL,
        gtk.MESSAGE_INFO,
        gtk.BUTTONS_CLOSE,
        msg)                            
    dialog.set_title(title)
    dialog.run()
    dialog.destroy()


def dialog_error(title,msg) :
    dialog = gtk.MessageDialog(None,
        gtk.DIALOG_MODAL,
        gtk.MESSAGE_ERROR,
        gtk.BUTTONS_CLOSE,
        msg)
    dialog.set_title(title)
    dialog.run()
    dialog.destroy()


def dialog_ask(title,msg) :
    dialog = gtk.MessageDialog(None,
        gtk.DIALOG_MODAL,
        gtk.MESSAGE_QUESTION,
        gtk.BUTTONS_YES_NO,
        msg)
    dialog.set_title(title)
    dialog.set_default_response(gtk.RESPONSE_YES)
    question = dialog.run()
    dialog.destroy()
    if (question == gtk.RESPONSE_YES) :
        return True
    return False

## End dialog
def dialog_end(warnC,errC,logFile,title,msg) :
    if (errC != 0) :
        msg += "\nError = " + str(errC)
        msg += "\nLog file = " + str(logFile)
        dialog_error(title, msg)
    else :
        if (warnC != 0) :
            msg += "\nWarning = " + str(warnC)
        msg += "\n\nLog file = " + str(logFile)
        dialog_info(title, msg)

###############################################






###############################################
###############################################
##             BASIC FUNCTIONS               ##
###############################################
###############################################

    
## Exit when receiving an exception
def sysKeybInt() :
    remove_lock_file()
    sys.exit(color_error + "\n#### Received Ctrl-C exception\n#### Quit properly" + color_reset)

## User login
def getUserLogin() :
    try :
        return os.environ['USER']
    except :
        print color_error + 'Cannot get the login user\n'
        sys.exit(-1)

def isDell():
    dell=0
    if os.environ.get('DELL') :
        dell=1
    else :
        # grep .cshrc to see if DELL is specified for graphic mode in Nemo
        for line in open (os.path.join(getHomeDir(), ".cshrc")) :
            if 'setenv DELL "1"' in line :
                dell=1
                break
    return dell

def getHomeDir():
    return expanduser("~")

def getBinDir():
    if isDell() :
        return os.path.join(getHomeDir(),"Perso/work/bin")
    else :
        return os.path.join(getHomeDir(),"Greg/work/bin")

def getEnvDir():
    if isDell() :
        return os.path.join(getHomeDir(),"Perso/work/env")
    else :
        return os.path.join(getHomeDir(),"Greg/work/env")

def getLogDir():
    return  os.path.join(getEnvDir(),"log")

## Get the human size of a file
def humanSize(num):
    for x in ['bytes','KB','MB','GB','TB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0

## Verify lock file
def verify_lock_file(lockFile) :
    timeout = 0
    ## Verify that the lock file doesn't exist
    while os.path.isfile(lockFile) :
        if (timeout > 200) :
            remove_lock_file(lockFile)
            break
        else :
            time.sleep(1)
            timeout += 1

## Create lock file
def create_lock_file(lockFile) :
    ## Verify that the lock file doesn't exist
    verify_lock_file(lockFile)
    ## Create it.
    os.system('touch ' + lockFile)

## Delete lock file
def remove_lock_file(lockFile) :
    ## Remove lock file
    try :
        os.remove(lockFile)
    except :
        pass

## Random number
def getRandomSeed() :
    return random.randint(1,65536)

## Create a integer range
def parseRange(rangestr) :
    result = list()
    try :
        if (rangestr!="") :
            list0=rangestr.split(",")
            for list1 in list0 :
                list2=list1.split("-")
                if (len(list2)==2) : #range found
                    for i in range(int(list2[0]),int(list2[1])+1) :
                        result.append(i)
                else :
                  result.append(int(list2[0]))
    except :
        parser.error(" There is a problem with your parsed options")

    return(result)

## Determine if the file is executable.
def filetest_exe(file) :
    """Determine if the file is executable."""
    if not os.path.exists(file):
        return 0
    stat = os.path.stat
    statinfo = os.stat(file)
    mode = stat.S_IMODE(statinfo[stat.ST_MODE])
    if ((stat.S_IXUSR & mode) or (stat.S_IXGRP & mode) or (stat.S_IXOTH & mode)):
        return True
    return False
    
## Remove a directory
def remove_dir_file(path) :
    list_files = os.listdir(path)
    for file in list_files :
        try :
            os.remove(os.path.join(path, file))
        except OSError:
            pass

## Move files in another directory
def move_files(old_path, new_path) :
    list_files = os.listdir(old_path)
    for file in list_files :
        try :
            os.rename(os.path.join(old_path, file), os.path.join(new_path, file))
        except :
            pass


def sendMail(From, To, Cc, Subject, Message):

    # Import smtplib for the actual sending function
    import smtplib
    # Import the email modules we'll need
    from email.mime.text import MIMEText

    msg = MIMEText(Message)

    msg['Subject'] = Subject
    msg['From'] = From
    msg['To'] = To
    msg['Cc'] = Cc
    
    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP('localhost')
    s.sendmail(From, [To], msg.as_string())
    s.quit()




###############################################
###############################################
##            ADVANCED FUNCTIONS             ##
###############################################
###############################################

def addFile(dbg, header, fileName, extAuth, typeList, warnNb) :
    dbg.info(header, "In  addFile fileName=" + str(fileName))
    dirN = os.path.dirname(fileName)
    dirN1=dirN.replace('(','\(')
    dirN2=dirN1.replace(')','\)')
    fileNameWoDir=re.sub(dirN2 + "\/", '', fileName)
    (fileN, extN) = os.path.splitext(fileNameWoDir)
    if extAuth.__contains__(extN) :
        dbg.info(header, "In  addFile dirN=" + str(dirN) + ", fileN=" + str(fileN) + ", extN=" + str(extN))
        typeList.append([dirN, fileN, extN])
        return (typeList, warnNb)
    else :
        warnNb += 1
        dbg.warn(header, "In  addFile file " + str(fileNameWoDir) + " is not a good extension as " + str(extAuth))
        return (typeList, warnNb)


def listFromArgs(dbg, header, args, ext) :
    dbg.info(header, "In  listFromArgs")
    typeList= list()
    warnNb = 0

    if (len(args) != 0) :
        for arg in args :
            arg.encode('latin1')
            if (os.path.isdir(arg)) :
                dirName = arg
                dbg.info(header, "In  listFromArgs dir=" + str(arg))
                for dirpath, dirnames, filenames in os.walk(arg) :
                    for filename in filenames :
                        (typeList, warnNb) = addFile(dbg, header, os.path.join(dirpath, filename), ext, typeList, warnNb)

            elif (os.path.isfile(arg)) :
                dbg.info(header, "In  listFromArgs file=" + str(arg))
                (typeList, warnNb) = addFile(dbg, header, arg, ext, typeList, warnNb)

    dbg.info(header, "Out listFromArgs typeList=" + str(typeList))
    return (typeList, warnNb)




###############################################
###############################################
##                  COLOR                    ##
###############################################
###############################################

## Color definition
color            = dict()
color['red']     ='\033[31m'
color['green']   ='\033[32m'
color['blue']    ='\033[34m'
color['magenta'] ='\033[35m'
color['cyan']    ='\033[36m'
color['reset']   ='\033[39m\033[49m\033[0m'
color['blink']   ='\033[5m'
color['bold']    ='\033[1m'
color_default    = color['cyan']

color_info1 = color['cyan']
color_info2 = color['green']
color_cmd   = color['magenta']
color_warn  = color['blue']
color_error = color['red']
color_reset = color['reset']

