#!/usr/bin/env python
# -*-coding:Latin-1 -*

'''
Screensaver Link

program to scan image files to determine different tags,
enable/disable whatever you want,
and create link for the screensaver.
'''





###############################################
# Graphical Libraries Imports
###############################################

# use for graphical interface
import sys
try :
    import pygtk
    pygtk.require('2.0')
except ImportError as e:
    sys.exit("Issue with PyGTK.\n" + str(e))
try :
    import gtk
except (RuntimeError, ImportError) as e:
    sys.exit("Issue with GTK.\n" + str(e))
try :
    import gobject
except (RuntimeError, ImportError) as e:
    sys.exit("Issue with GOBJECT.\n" + str(e))

from gtk import RESPONSE_YES, RESPONSE_NO


###############################################
# Basic Imports
###############################################

# default system
import os, os.path
import re
from optparse import OptionParser

## common
from python_common import *
HEADER = "screensaverLink"

## directory
homeDir = getHomeDir()
logDir  = getLogDir()

###############################################



###############################################
## Global variables
###############################################

t = str(datetime.datetime.today().isoformat("_"))
logFile = os.path.join(logDir, HEADER + "_" + t + ".log")
lockFile = os.path.join(logDir, HEADER + ".lock")

progIcon = "screensaverLink.png"
imagesDir = os.path.join(homeDir, ".screensaverLink")
linkDir = os.path.join(homeDir, ".screensaverLink")

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
    help    = "Don't launch the gui"
    )

(parsedArgs , args) = parser.parse_args()

###############################################



###############################################
###############################################
##                  CLASS                    ##
###############################################
###############################################


class GuiC(gtk.Window) :

    def __init__(self, logC) :
        self.log = logC


    def run(self):
        self.log.info("In  run", HEADER)
        # create the main window
        self.createWin()
        
        # display it
        gtk.main()
        self.log.info("Out run", HEADER)


    def on_destroy(self, widget):
        gtk.main_quit()
        

    def createWin(self):
        self.log.info("In  createWin", HEADER)

        #
        # Main window
        #

        gtk.Window.__init__(self)
        try :
            self.set_icon_from_file(progIcon)
        except gobject.GError :
            pass
        self.connect("destroy", self.on_destroy)

        self.set_title("Screensaver Images Tags")
        self.set_border_width(5)
        self.set_default_size(400, 600)


        #
        # Vertical box = tag list + buttons
        #
        vTagBut = gtk.VBox(False, 15)
        vTagBut.set_border_width(5)
        self.add(vTagBut)


        # Tag list
        #

        # Create the scrolled windows
        tagsSw = gtk.ScrolledWindow()
        tagsSw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        tagsSw.set_shadow_type(gtk.SHADOW_IN)

        # Create tags treeview
        tagsTv = gtk.TreeView(gtk.TreeStore(gobject.TYPE_STRING))
        tagsSw.add(tagsTv)

        vTagBut.pack_start(tagsSw, True, True)



        # Buttons
        #

        # Create the buttons
        butTab = gtk.Table(2, 4, True)
        butTab.set_row_spacings(10)
        butTab.set_col_spacings(10)

        # scan tags
        gtk.stock_add([(gtk.STOCK_REFRESH, "Scan tags", 0, 0, "")])
        scanBut = gtk.Button(stock=gtk.STOCK_REFRESH)
        #scanBut.connect("clicked", self.winCfgsC.on_clicked_config_add)
        butTab.attach(scanBut, 0, 2, 0, 1)
        # create links
        gtk.stock_add([(gtk.STOCK_EXECUTE, "Create links", 0, 0, "")])
        exeBut = gtk.Button(stock=gtk.STOCK_EXECUTE)
        #exeBut.connect("clicked", self.winCfgsC.on_clicked_config_save)
        butTab.attach(exeBut, 2, 4, 0, 1)
        # quit
        quitBut = gtk.Button(stock=gtk.STOCK_CLOSE)
        quitBut.connect("clicked", self.on_destroy)
        butTab.attach(quitBut, 1, 3, 1, 2)

        vTagBut.pack_start(butTab, False, False, 0)


        # Display the window
        self.show_all()

        self.log.info("Out createWin", HEADER)





###############################################







###############################################
###############################################
###############################################
##                 MAIN                      ##
###############################################
###############################################
###############################################


def main() :
    ## Create self.log class
    global log
    log = LOGC(logFile, HEADER, parsedArgs.debug, parsedArgs.gui)

    ## Graphic interface
    gui = GuiC(log)
    gui.run()



if __name__ == '__main__':
    main()

###############################################

