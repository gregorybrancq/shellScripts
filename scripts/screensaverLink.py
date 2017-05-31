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

    def __init__(self, self.logC) :
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

        gtk.Window.__init__(self)
        try :
            self.set_icon_from_file(progIcon)
        except gobject.GError :
            pass
        self.connect("destroy", self.on_destroy)

        self.set_title("Screensaver Images Tags")
        self.set_border_width(5)
        self.set_default_size(800, 700)


        #
        # Create the vertical box
        #   the tag box & the buttons
        #
        vBoxLeft = gtk.VBox(False, 20)
        vBoxLeft.set_border_width(5)

        #
        # Vertical box
        #
        frameConfig = gtk.Frame()
        frameConfig.set_label("Configurations")
        vBoxConfig = gtk.VBox(False, 15)
        vBoxConfig.set_border_width(5)

        #
        # Create the tool's tab
        #

        # Create the scrolled windows
        tools_sw = gtk.ScrolledWindow()
        # tools_sw.set_policy(gtk.PolicyType.AUTOMATIC, gtk.PolicyType.AUTOMATIC)
        tools_sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        # tools_sw.set_shadow_type(Gtk.ShadowType.IN)
        tools_sw.set_shadow_type(gtk.SHADOW_IN)
        # tools_sw.set_min_content_height(150)
        # tools_sw.set_min_content_width(350)

        # Create tools treeview
        toolTV = self.winToolsC.create_tool_treeview()
        tools_sw.add(toolTV)


        # Create the configuration scrolled windows
        left_sw = gtk.ScrolledWindow()
        # left_sw.set_min_content_height(100)
        # left_sw.set_min_content_width(100)
        left_sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        left_sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        # with the config list inside

        # Create the config treeview
        configTV = self.winCfgsC.create_config_treeview()
        left_sw.add(configTV)
        vBoxConfig.pack_start(left_sw, True, True)


        # Create the buttons
        tabButConf = gtk.Table(3, 3, True)
        tabButConf.set_row_spacings(10)
        tabButConf.set_col_spacings(10)

        # new
        button_addC = gtk.Button(stock=gtk.STOCK_ADD)
        button_addC.connect("clicked", self.winCfgsC.on_clicked_config_add)
        tabButConf.attach(button_addC, 0, 1, 0, 1)
        # copy
        button_copyC = gtk.Button(stock=gtk.STOCK_COPY)
        button_copyC.connect("clicked", self.winCfgsC.on_clicked_config_copy)
        tabButConf.attach(button_copyC, 1, 2, 0, 1)
        # delete
        button_delC = gtk.Button(stock=gtk.STOCK_DELETE)
        button_delC.connect("clicked", self.winCfgsC.on_clicked_config_delete)
        tabButConf.attach(button_delC, 2, 3, 0, 1)
        # use config
        button_useC = gtk.Button("_Use", use_underline=True)
        button_useC.connect("clicked", self.winCfgsC.on_clicked_config_use)
        tabButConf.attach(button_useC, 0, 1, 1, 2)
        # init config
        button_initC = gtk.Button("_Init", use_underline=True)
        button_initC.connect("clicked", self.winCfgsC.on_clicked_config_init)
        tabButConf.attach(button_initC, 1, 2, 1, 2)
        # apply
        button_applyC = gtk.Button("Save", use_underline=True)
        button_applyC.connect("clicked", self.winCfgsC.on_clicked_config_save)
        tabButConf.attach(button_applyC, 2, 3, 1, 2)
        # quit
        button_applyC = gtk.Button(stock=gtk.STOCK_CLOSE)
        button_applyC.connect("clicked", self.on_destroy)
        tabButConf.attach(button_applyC, 1, 2, 2, 3)

        vBoxConfig.pack_start(tabButConf, False, False, 0)
        frameConfig.add(vBoxConfig)
        vBoxLeft.pack_start(frameConfig, True, True, 0)


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
    log = self.logC(logFile, HEADER, parsedArgs.debug, parsedArgs.gui)

    ## Graphic interface
    gui = GuiC(log)
    gui.init()



if __name__ == '__main__':
    main()

###############################################

