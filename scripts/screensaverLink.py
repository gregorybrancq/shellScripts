#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Screensaver Link

program to scan image files to determine different tags,
enable/disable whatever you want,
and create link for the screensaver.

see screensaverLink_body.xml to know xml format example.

'''





###############################################
# Imports
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

# default system
import os, os.path
import re
import shutil
from optparse import OptionParser

# tags for image
from PIL import Image

# xml
import xml.etree.ElementTree as ET
from lxml import etree

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
imagesDir = os.path.join(homeDir, "Test")
linkDir = os.path.join(homeDir, "Screensaver")
configDir = os.path.join(homeDir, "Greg", "work", "config", "screensaverLink")
configName = "config.xml"
configN = os.path.join(configDir, configName)


## Tag Columns
(
  COL_NAME,
  COL_ENABLE,
  COL_ENABLE_VISIBLE,
  COL_ENABLE_ACTIVATABLE
) = range(4)

COL_CHILDREN = 4


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


class ConfigTagC() :

    def __init__(self, logC) :
        self.log = logC





class TagC() :

    def __init__(self, logC) :
        self.log = logC
        self.tagDict = dict() # [tagName] = Enable
        self.fileDict = dict() # [fileName] = tagList


    def __str__(self) :
        res = "\n"
        res += "#-----------------\n"
        res += "# Tags\n"
        res += "#-----------------\n"
        tagsN = self.getTags()
        for tagN in tagsN :
            res += str(tagN) + " : " + str(self.tagDict[tagN]) + "\n"
        res += "\n\n"

        res += "#-----------------\n"
        res += "# Files\n"
        res += "#-----------------\n"
        fileNSort = self.getFiles()
        fileNSort.sort()
        for fileN in fileNSort :
            res += str(fileN) + " : "
            for tagN in self.fileDict[fileN] :
                res += str(tagN) + ", "
            res += "\n"
        res += "\n"

        return res


    def init(self) :
        self.scanTags()
        self.readConfig()


    def getTags(self) :
        tagsNSort = self.tagDict.keys()
        tagsNSort.sort()
        return tagsNSort


    def getTagEn(self, tagN) :
        return self.tagDict[tagN]


    def setTagEn(self, tagN, en) :
        self.tagDict[tagN] = en


    def getFiles(self) :
        return self.fileDict.keys()


    # Return tags with a two-level ordered
    def getTagsByHier(self) :
        resDict = dict()
        for tagN in self.getTags() :
            (lvl1, lvl2) = re.split("/", tagN)
            tagEn = self.getTagEn(tagN)
            if not resDict.has_key(lvl1) :
                #self.log.dbg("In  getTagsByHier add lvl1="+str(lvl1)+" lvl2="+str(lvl2)+" tagEn="+str(tagEn))
                l = list()
                l.append([lvl2, tagEn])
                resDict[lvl1] = [[lvl2, tagEn]]
                #self.log.dbg("In  getTagsByHier resDict="+str(resDict))
            else :
                tagList = resDict[lvl1]
                find = False

                #self.log.dbg("In  getTagsByHier tagList="+str(tagList))
                for tagLvl2 in tagList :
                    #self.log.dbg("In  getTagsByHier tagLvl2="+str(tagLvl2))
                    if tagLvl2[0] == lvl2 :
                        find = True
                        break

                if not find :
                    tagList.append([lvl2, tagEn])

        self.log.dbg("In  getTagsByHier res="+str(resDict))
        return resDict


    ## read tools configuration file
    def readConfig(self) :
        self.log.info(HEADER, "In  readConfig " + configN)

        if not os.path.isfile(configN) :
            self.log.info(HEADER, "In  readConfig config file doesn't exist.")
            self.writeConfig()

        else :
            # Open config file
            tree = ET.parse(configN).getroot()

            for tagN in tree.iter("tag") :
                tagName = None
                tagEnable = None

                # Get tag name
                if "name" in tagN.attrib :
                    tagName = tagN.attrib["name"]
                # Get tag enable
                if "enable" in tagN.attrib :
                    tagEnable = tagN.attrib["enable"]
                
                self.updateTag(tagName, tagEnable)

        self.log.info(HEADER, "Out readConfig")


    ## write tools configuration file
    def writeConfig(self) :
        self.log.info(HEADER, "In  writeConfig " + configN)
        
        tagsTree = etree.Element("tags")
        tagsTree.addprevious(etree.Comment("!!! Don't modify this file !!!"))
        tagsTree.addprevious(etree.Comment("Managed by " + HEADER))
            
        tagsN = self.getTags()
        for tagN in tagsN :
            # Create the element tree
            self.log.dbg("In  writeConfig tagN="+str(tagN)+" enable="+str(self.tagDict[tagN]))
            tagTree = etree.SubElement(tagsTree, "tag")
            tagTree.set("name", tagN)
            tagTree.set("enable", str(self.tagDict[tagN]))
        
        # Save to XML file
        doc = etree.ElementTree(tagsTree)
        doc.write(configN, encoding='utf-8', method="xml", pretty_print=True, xml_declaration=True) 
            
        self.log.info(HEADER, "Out writeConfig " + configN)


    def updateTag(self, tagN, tagE) :
        if self.tagDict.has_key(tagN) :
            if tagE == 'True' :
                self.tagDict[tagN] = True
            elif tagE == 'False' :
                self.tagDict[tagN] = False


    def addTagFile(self, tagN, fileN) :
        if not self.tagDict.has_key(tagN) :
            self.log.dbg("In  addTagFile tag "+str(tagN)+" doesn't exist")
            self.tagDict[tagN] = True

        if not self.fileDict.has_key(fileN) :
            self.log.dbg("In  addTagFile file "+str(fileN)+" doesn't exist")
            tagList = list()
            tagList.append(tagN)
            self.fileDict[fileN] = tagList
        else :
            self.log.dbg("In  addTagFile file "+str(fileN)+" already exist")
            tagList = self.fileDict[fileN]
            if not tagList.__contains__(tagN) :
                tagList.append(tagN)


    def readTag(self, fileN) :
        with Image.open(fileN) as im:
            for segment, content in im.applist:
                marker, body = content.split('\x00', 1)
                if segment == 'APP1' and marker == 'http://ns.adobe.com/xap/1.0/' :
                    root = ET.fromstring(body)

                    for levelRDF in root :
                        #print "LevelRDF=" + levelRDF.tag
                        for levelDescription in levelRDF :
                            #print "levelDescription.tag=" + levelDescription.tag
                            for levelTagsList in levelDescription :
                                #print "levelTagsList.tag=" + levelTagsList.tag
                                if levelTagsList.tag == "{http://www.digikam.org/ns/1.0/}TagsList" :
                                    for levelSeq in levelTagsList :
                                        #print "levelSeq.tag=" + levelSeq.tag
                                        for levelLi in levelSeq :
                                            self.addTagFile(levelLi.text, fileN)


    def scanTags(self) :
        self.log.info(HEADER, "In  scanTags")
        if os.path.isdir(imagesDir) :
            for dirpath, dirnames, filenames in os.walk(imagesDir) :  # @UnusedVariable
                self.log.dbg("In  scanTags dirpath="+str(dirpath)+" dirnames="+str(dirnames)+" filenames="+str(filenames))
                if filenames.__len__ != 0 :
                    for filename in filenames :
                        fileWithPath = os.path.join(dirpath, filename)
                        self.readTag(fileWithPath)
        self.log.info(HEADER, "Out scanTags")


    def createLinks(self) :
        self.log.info(HEADER, "In  createLinks")
        # delete link directory
        if os.path.isdir(linkDir) :
            shutil.rmtree(linkDir)
        os.makedirs(linkDir)

        for fileN in self.fileDict :
            # should be install ?
            install = True
            tagList = self.fileDict[fileN]
            for tagN in tagList :
                if not self.tagDict[tagN] :
                    install = False
                    break

            if install :
                curDir = os.getcwd()
                os.chdir(linkDir)

                # create link name
                linkN = re.sub(homeDir, "", fileN)
                linkN = re.sub("/", "_", linkN)
                linkN = re.sub("^_", "", linkN)
                os.symlink(fileN, linkN)
                self.log.dbg("In  createLinks file="+str(fileN)+" linkN="+str(linkN))
        
        self.log.info(HEADER, "Out createLinks")








class GuiC(gtk.Window) :

    def __init__(self, logC) :
        self.log = logC
        self.tagC = TagC(self.log)
        self.tagGuiC = TagGuiC(self.tagC, self.log)


    def run(self):
        self.log.info(HEADER, "In  run")

        self.tagC.init()
        # DBGprint str(self.tagC)

        if parsedArgs.gui :
            # create the main window
            self.createWin()
            
            # display it
            gtk.main()

        self.log.info(HEADER, "Out run")


    def on_destroy(self, widget):
        gtk.main_quit()
        

    def createWin(self):
        self.log.info(HEADER, "In  createWin")

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
        tagsSw.add(self.tagGuiC.createTagTv())

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
        scanBut.connect("clicked", self.onScan)
        butTab.attach(scanBut, 0, 2, 0, 1)
        # create links
        gtk.stock_add([(gtk.STOCK_EXECUTE, "Create links", 0, 0, "")])
        exeBut = gtk.Button(stock=gtk.STOCK_EXECUTE)
        exeBut.connect("clicked", self.onExecute)
        butTab.attach(exeBut, 2, 4, 0, 1)
        # quit
        quitBut = gtk.Button(stock=gtk.STOCK_CLOSE)
        quitBut.connect("clicked", self.on_destroy)
        butTab.attach(quitBut, 1, 3, 1, 2)

        vTagBut.pack_start(butTab, False, False, 0)

        # Display the window
        self.show_all()

        self.log.info(HEADER, "Out createWin")


    def onScan(self, button=None) :
        self.tagC.scanTags()


    def onExecute(self, button=None) :
        self.tagC.writeConfig()
        self.tagC.createLinks()







class TagGuiC() :

    def __init__(self, tagC, logC) :
        self.log = logC
        self.tagC = tagC
        self.model = self.initModel()
        self.treeselect = gtk.TreeView()
        self.memColEn = "current"
        self.selLvl1 = str()
        self.selLvl2 = str()
        self.selEn = bool()


    def initModel(self) :
        # create tree store
        return gtk.TreeStore(
                    gobject.TYPE_STRING,
                    gobject.TYPE_BOOLEAN,
                    gobject.TYPE_BOOLEAN,
                    gobject.TYPE_BOOLEAN)


    def createTagTv(self) :
        self.log.info(HEADER, "In  createTagTv")

        # create model
        self.createModel()

        # create tag treeview
        treeview = gtk.TreeView(self.model)
        treeview.set_rules_hint(True)
        treeview = self.addCol(treeview)

        self.treeselect = treeview.get_selection()
        self.treeselect.set_mode(gtk.SELECTION_SINGLE)
        self.treeselect.connect('changed', self.onChanged)

        self.log.info(HEADER, "Out createTagTv")
        return treeview


    def createModel(self) :
        self.log.info(HEADER, "In  createModel")
        topLvl = list()
        self.model.clear()

        # Construct list to put in model 
        tagsDict = self.tagC.getTagsByHier()
        for tag in tagsDict :
            #self.log.dbg("In  createModel lvl1="+str(tag))

            ## Level 2
            lvl2L = list()
            for lvl2 in tagsDict[tag] :
                #self.log.dbg("In  createModel lvl2="+str(lvl2))
                lvl2info = list()

                # name
                lvl2info.append(lvl2[0])
                # enable
                lvl2info.append(lvl2[1])
                # visible
                lvl2info.append(True)
                # activatable
                lvl2info.append(True)
                #self.log.dbg("In  createModel lvl2info="+str(lvl2info))

                lvl2L.append(lvl2info)

            ## Level 1
            lvl1L = list()
            # name
            lvl1L.append(tag)
            # enable
            lvl1L.append(False)
            # visible
            lvl1L.append(False)
            # activatable
            lvl1L.append(False)
            #self.log.dbg("In  createModel lvl1L="+str(lvl1L))

            # Add Version
            lvl1L.append(lvl2L)

            topLvl.append(lvl1L)


        ## Add data to the tree store
        self.log.dbg("In  createModel topLvl="+str(topLvl))
        for tag in topLvl :
            tagIter = self.model.append(None)

            self.model.set(tagIter,
                COL_NAME, tag[COL_NAME],
                COL_ENABLE, tag[COL_ENABLE],
                COL_ENABLE_VISIBLE, tag[COL_ENABLE_VISIBLE],
                COL_ENABLE_ACTIVATABLE, tag[COL_ENABLE_ACTIVATABLE]
            )

            for lvl2 in tag[COL_CHILDREN] :
                versionIter = self.model.append(tagIter)
                self.model.set(versionIter,
                    COL_NAME, lvl2[COL_NAME],
                    COL_ENABLE, lvl2[COL_ENABLE],
                    COL_ENABLE_VISIBLE, lvl2[COL_ENABLE_VISIBLE],
                    COL_ENABLE_ACTIVATABLE, lvl2[COL_ENABLE_ACTIVATABLE]
                )

        self.log.info(HEADER, "Out createModel")


    def addCol(self, treeview) :
        self.log.info(HEADER, "In  addCol")
        model = treeview.get_model()

        # Column for tag's enable
        renderer = gtk.CellRendererToggle()
        renderer.set_property("xalign", 0.0)
        renderer.connect("toggled", self.onToggledItem, model)
        column = gtk.TreeViewColumn("Enable", renderer, active=COL_ENABLE,
                                    visible=COL_ENABLE_VISIBLE, activatable=COL_ENABLE_ACTIVATABLE)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column.set_clickable(True)
        column.set_fixed_width(60)
        column.connect("clicked", self.onColEnable, model)

        treeview.append_column(column)

        # Column for tag's name
        renderer = gtk.CellRendererText()
        renderer.set_property("xalign", 0.0)
        column = gtk.TreeViewColumn("Name", renderer, text=COL_NAME)
        column.set_clickable(False)

        treeview.append_column(column)
        self.log.info(HEADER, "Out addCol")
        return treeview


    # When the user clicks on the column "enable"
    def onColEnable(self, cell, model) :
        self.log.info(HEADER, "In  onColEnable")

        if self.memColEn == "all" :
            self.memColEn = "none"
        elif self.memColEn == "none" :
            self.memColEn = "current"
        elif self.memColEn == "current" :
            self.memColEn = "all"

        for tagN in self.tagC.getTags() :
            if self.memColEn == "all" :
                self.tagC.setTagEn(tagN, True)
            elif self.memColEn == "none" :
                self.tagC.setTagEn(tagN, False)
            elif self.memColEn == "current" :
                self.tagC.readConfig()

        # update model
        self.createModel()

        self.log.info(HEADER, "Out onColEnable")


    # each time selection changes, this function is called
    def onChanged(self, selection) :
        self.log.info(HEADER, "In  onChanged")

        model, rows = selection.get_selected_rows()

        for row in rows :
            iterSel = model.get_iter(row)
            iterSel_has_child = model.iter_has_child(iterSel)

            if iterSel_has_child :
                self.selLvl1 = model.get_value(iterSel, COL_NAME)
                self.selLvl2 = None
                self.selEn = False
            elif not iterSel_has_child :
                iterSelParent = model.iter_parent(iterSel)
                self.selLvl1 = model.get_value(iterSelParent, COL_NAME)
                self.selLvl2 = model.get_value(iterSel, COL_NAME)
                self.selEn = model.get_value(iterSel, COL_ENABLE)
        
        self.log.dbg("selLvl1=" + str(self.selLvl1))
        self.log.dbg("selLvl2=" + str(self.selLvl2))
        self.log.dbg("selEn=" + str(self.selEn))
        self.log.info(HEADER, "Out onChanged")


    # When user clicks on a box
    def onToggledItem(self, cell, path_str, model) :
        self.log.info(HEADER, "In  onToggledItem")

        iterSel = model.get_iter_from_string(path_str)
        selIsTool = model.iter_has_child(iterSel)
        
        # Get enable column (before click)
        selEnable = model.get_value(iterSel, COL_ENABLE)
        # Get lvl2 name
        selLvl2 = model.get_value(iterSel, COL_NAME)
        # Get lvl1 name
        iterSelParent = model.iter_parent(iterSel)
        selLvl1 = model.get_value(iterSelParent, COL_NAME)
        # Set tag name
        selTagN = selLvl1 + "/" + selLvl2

        self.log.dbg("selLvl1=" + str(selLvl1))
        self.log.dbg("selLvl2=" + str(selLvl2))
        self.log.dbg("selEnable=" + str(selEnable))

        # Disable
        # From True to False (as value is before clicking)
        if selEnable :
            self.tagC.setTagEn(selTagN, False)
            model.set(iterSel, COL_ENABLE, False)
            self.log.dbg("not install " + str(selTagN))

        # Enable
        # From False to True
        else :
            self.tagC.setTagEn(selTagN, True)
            model.set(iterSel, COL_ENABLE, True)
            self.log.dbg("install " + str(selTagN))

        self.log.info(HEADER, "Out onToggledItem")


###############################################







###############################################
###############################################
###############################################
##                 MAIN                      ##
###############################################
###############################################
###############################################


def main() :
    ## Create log class
    global log
    log = LOGC(logFile, HEADER, parsedArgs.debug, parsedArgs.gui)

    ## Graphic interface
    gui = GuiC(log)
    gui.run()



if __name__ == '__main__':
    main()

###############################################

