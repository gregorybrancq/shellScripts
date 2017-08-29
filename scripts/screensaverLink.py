#!/usr/bin/env python
# coding: utf-8

'''
Screensaver Link

program to scan image files to determine different tags,
enable/disable whatever you want,
and create link for the screensaver.

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

progIcon = os.path.join(homeDir, "Greg", "work", "config", "icons", "screensaverLink.png")
imagesDir = os.path.join(homeDir, "Images")
#imagesDir = os.path.join(homeDir, "Greg", "work", "config", "screensaverLink", "Test")
linkDir = os.path.join(homeDir, "Screensaver")
#linkDir = os.path.join(homeDir, "Screensaver_test")
configDir = os.path.join(homeDir, "Greg", "work", "config", "screensaverLink")
configName = "config.xml"
#configName = "config_test.xml"
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


class TagC() :

    def __init__(self, logC) :
        self.log = logC
        self.tagDict = dict() # [tagName] = enable
        self.tagMultiList = list() # [tagname0, enable0], [tagname1, disable1], enable ]
        self.fileDict = dict() # [fileName] = tagList


    def __str__(self) :
        res = "\n"
        res += "#-----------------\n"
        res += "# Simple Tags\n"
        res += "#-----------------\n"
        tagsN = self.getSimpleTags()
        for tagN in tagsN :
            res += str(tagN) + " : " + str(self.tagDict[tagN]) + "\n"
        res += "\n\n"

        res += "#-----------------\n"
        res += "# Multiple Tags\n"
        res += "#-----------------\n"
        i = 1
        for tagsEnM in self.tagMultiList :
            res += "Tags " + str(i) + " enable=" + str(tagsEnM[1])  + "\n  "
            for tagM in tagsEnM[0] :
                res += str(tagM[0]) + " : " + str(tagM[1]) + ", "
            res += "\n"
            i += 1
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


    def convertStrToBool(self, pattern) :
        # be sure string is a boolean
        if isinstance(pattern, str) :
            if pattern == 'True' :
                pattern = True
            else :
                pattern = False
        return pattern


    def getSimpleTags(self) :
        tagsNSort = self.tagDict.keys()
        tagsNSort.sort()
        return tagsNSort


    def getSimpleTagEn(self, tagN) :
        return self.tagDict[tagN]


    def setSimpleTagEn(self, tagN, tagEn) :
        self.tagDict[tagN.decode('utf-8')] = tagEn
        #self.log.dbg("Out setSimpleTagEn tagDict="+str(self.tagDict))


    def getFiles(self) :
        filesNSort = self.fileDict.keys()
        filesNSort.sort()
        return filesNSort


    def getFileTagsL(self, fileN) :
        tagsL = self.fileDict[fileN]
        tagsL.sort()
        return tagsL


    def addSimpleTag(self, tagN, tagEn) :
        self.log.dbg("In  addSimpleTag tagN="+str(tagN)+" tagEn="+str(tagEn))
        tagEn = self.convertStrToBool(tagEn)
        self.setSimpleTagEn(tagN, tagEn)
        self.log.dbg("Out addSimpleTag tagDict="+str(self.tagDict))


    def isAlreadyInMultiTag(self, tagMulti) :
        self.log.dbg("In  isAlreadyInMultiTag tagMulti="+str(tagMulti))
        found = False

        # Sort it
        tagMulti.sort()
        
        # Find
        for tagsEnM in self.tagMultiList :
            #self.log.dbg("In  isAlreadyInMultiTag tagsEnM="+str(tagsEnM))
            i = 0
            tagsM = tagsEnM[0]
            #self.log.dbg("In  isAlreadyInMultiTag tagsM="+str(tagsM))
            if tagsM.__len__() == tagMulti.__len__() :
                #self.log.dbg("In  isAlreadyInMultiTag same length tagsM="+str(tagsM))
                for tagM in tagsM :
                    #self.log.dbg("In  isAlreadyInMultiTag tagM="+str(tagM))
                    if tagM[0] == tagMulti[i][0] :
                        i += 1
                        #self.log.dbg("In  isAlreadyInMultiTag i="+str(i))
                    else :
                        i = 0
                        #self.log.dbg("In  isAlreadyInMultiTag i="+str(i))
                        break

            #self.log.dbg("In  isAlreadyInMultiTag i="+str(i))
            if (i == tagMulti.__len__()) :
                found = True
                break

        self.log.dbg("Out isAlreadyInMultiTag found=" + str(found))
        return found


    # With a tag name (included with + and -), 
    # it will return the element or None
    def findElt(self, tagName) :
        #self.log.dbg("In  findElt tagMultiList=" + str(self.tagMultiList))
        foundElt = None
        for tagsEnM in self.tagMultiList :
            #self.log.dbg("In  findElt tagsEnM=" + str(tagsEnM))
            newTagN = tagName
            for tagM in tagsEnM[0] :
                #self.log.dbg("In  findElt tagM=" + str(tagM))
                #self.log.dbg("In  findElt tagM[0]=" + str(tagM[0]))
                #self.log.dbg("In  findElt newTagN=" + str(newTagN))
                if re.search(tagM[0], newTagN) :
                    #self.log.dbg("In  findElt 1 newTagN=" + str(newTagN))
                    newTagN = re.sub(tagM[0], "", newTagN)
                    #self.log.dbg("In  findElt 2 newTagN=" + str(newTagN))
                else :
                    break
            #self.log.dbg("In  findElt 3 newTagN=" + str(newTagN))

            newTagN = re.sub("\+|\-| ", "", newTagN)
            if newTagN == "" :
                #self.log.dbg("In  findElt tagsEnM=" + str(tagsEnM))
                foundElt = tagsEnM
                break
        
        self.log.dbg("In  findElt tagsEnM=" + str(tagsEnM))
        return foundElt


    # With a tag name (included with + and -), 
    # it will set enable/disable value
    def setEnOnMulti(self, tagName, tagEn) :
        self.log.dbg("In  setEnOnMulti tagName=" + str(tagName) + ", tagEn=" + str(tagEn))
        foundElt = self.findElt(tagName)
        if foundElt is not None :
            self.tagMultiList.remove(foundElt)
            self.addMultiTag(foundElt[0], tagEn)


    def addMultiTag(self, tagL, tagEn) :
        self.log.dbg("In  addMultiTag tagL="+str(tagL)+", tagEn="+str(tagEn))
        # be sure tagEn is a boolean
        tagEn = self.convertStrToBool(tagEn)

        # Decode name
        newTagL = list()
        for tag in tagL :
            #self.log.dbg("In  addMultiTag tag="+str(tag))
            tag[1] = self.convertStrToBool(tag[1])
            newTagL.append([tag[0].decode('utf-8'), tag[1]])
        #self.log.dbg("In  addMultiTag newTagL="+str(newTagL))

        # Already exists ?
        if not self.isAlreadyInMultiTag(newTagL) :
            #self.log.dbg("In  addMultiTag tagEn="+str(tagEn))
            self.tagMultiList.append([newTagL, tagEn])
            self.tagMultiList.sort()


    def addFileAndTags(self, fileN, tagN) :
        self.log.dbg("In  addFileAndTags fileN="+str(fileN)+ " tagN="+str(tagN))
        fileNDec = fileN.decode('utf-8')
        tagNDec = tagN.decode('utf-8')
        if not self.fileDict.has_key(fileNDec) :
            tagList = list()
            tagList.append(tagNDec)
            self.fileDict[fileNDec] = tagList
        else :
            tagList = self.fileDict[fileNDec]
            if not tagList.__contains__(tagNDec) :
                tagList.append(tagNDec)


    # Return tags with a two-level ordered
    def getSimpleTagsByHier(self) :
        resDict = dict()
        for tagN in self.getSimpleTags() :
            (lvl1, lvl2) = re.split("/", tagN)
            tagEn = self.getSimpleTagEn(tagN)
            if not resDict.has_key(lvl1) :
                #self.log.dbg("In  getSimpleTagsByHier add lvl1="+str(lvl1)+" lvl2="+str(lvl2)+" tagEn="+str(tagEn))
                l = list()
                l.append([lvl2, tagEn])
                resDict[lvl1] = [[lvl2, tagEn]]
                #self.log.dbg("In  getSimpleTagsByHier resDict="+str(resDict))
            else :
                tagsList = resDict[lvl1]
                find = False

                #self.log.dbg("In  getSimpleTagsByHier tagsList="+str(tagsList))
                for tagLvl2 in tagsList :
                    #self.log.dbg("In  getSimpleTagsByHier tagLvl2="+str(tagLvl2))
                    if tagLvl2[0] == lvl2 :
                        find = True
                        break

                if not find :
                    tagsList.append([lvl2, tagEn])

        self.log.dbg("In  getSimpleTagsByHier res="+str(resDict))
        return resDict


    ## read tools configuration file
    def readConfig(self) :
        self.log.info(HEADER, "In  readConfig " + configN)

        if not os.path.isfile(configN) :
            self.log.info(HEADER, "In  readConfig config file doesn't exist.")
            self.writeConfig()

        else :
            # Initialize variables
            self.tagDict = dict()
            self.tagMultiList = list()

            # Open config file
            tree = ET.parse(configN).getroot()

            # Simple Tags part
            for simpleTagTree in tree.iter("simpleTag") :
                tagName = None
                tagEnable = None

                # Get tag name
                if "name" in simpleTagTree.attrib :
                    tagName = simpleTagTree.attrib["name"]
                # Get tag enable
                if "enable" in simpleTagTree.attrib :
                    tagEnable = simpleTagTree.attrib["enable"]
                
                self.addSimpleTag(tagName, tagEnable)

            # Multiple Tags part
            for multiTagsTree in tree.iter("multiTags") :
                tagsEnable = None

                # Get tag enable
                if "enable" in multiTagsTree.attrib :
                    tagsEnable = multiTagsTree.attrib["enable"]

                # Find multi tag
                tagsL = list()
                for multiTagTree in multiTagsTree.iter("multiTag") :
                    tagName = None
                    tagEnable = None

                    # Get tag name
                    if "name" in multiTagTree.attrib :
                        tagName = multiTagTree.attrib["name"]
                    # Get tag enable
                    if "enable" in multiTagTree.attrib :
                        tagEnable = multiTagTree.attrib["enable"]
                    tagsL.append([tagName, tagEnable])
                
                self.addMultiTag(tagsL, tagsEnable)

            # Files part
            for fileTree in tree.iter("file") :
                fileName = None
                # Get file name
                if "name" in fileTree.attrib :
                    fileName = fileTree.attrib["name"]
                # Find file tags
                for tagTree in fileTree.iter("fileTag") :
                    tagName = tagTree.text
                    self.addFileAndTags(fileName, tagName)

        self.log.info(HEADER, "Out readConfig")


    ## write tools configuration file
    def writeConfig(self) :
        self.log.info(HEADER, "In  writeConfig " + configN)
        
        tagsAndFilesTree = etree.Element("TagsFiles")
        tagsAndFilesTree.addprevious(etree.Comment("!!! Don't modify this file !!!"))
        tagsAndFilesTree.addprevious(etree.Comment("Managed by " + HEADER))

        # Simple Tags part
        simpleTagsTree = etree.SubElement(tagsAndFilesTree, "simpleTags")
        tagsN = self.getSimpleTags()
        #self.log.dbg("In  writeConfig tagsN="+str(tagsN))
        for tagN in tagsN :
            # Create the element tree
            #self.log.dbg("In  writeConfig tagN="+str(tagN)+" enable="+str(self.getSimpleTagEn(tagN)))
            tagTree = etree.SubElement(simpleTagsTree, "simpleTag")
            tagTree.set("name", tagN)
            tagTree.set("enable", str(self.getSimpleTagEn(tagN)))
          
        # Multiple Tags part
        multiTagsTree = etree.SubElement(tagsAndFilesTree, "multiTagsTree")
        for tagsEnM in self.tagMultiList :
            #self.log.dbg("In  writeConfig multiTag="+str(tagsEnM[0])+" enable="+str(tagsEnM[1]))
            # Create the element tree
            multiTagsT = etree.SubElement(multiTagsTree, "multiTags")
            multiTagsT.set("enable", str(tagsEnM[1]))
            for tagM in tagsEnM[0] :
                #self.log.dbg("In  writeConfig tagN="+str(tagM[0])+" enable="+str(tagM[1]))
                multiTagT = etree.SubElement(multiTagsT, "multiTag")
                multiTagT.set("name", tagM[0])
                multiTagT.set("enable", str(tagM[1]))

        # Files part
        filesTree = etree.SubElement(tagsAndFilesTree, "files")
        filesN = self.getFiles()
        for fileN in filesN :
            # Create the element tree
            #self.log.dbg("In  writeConfig fileN="+str(fileN)+" tagsList="+str(self.getFileTagsL(fileN)))
            tagsFTree = etree.SubElement(filesTree, "file")
            tagsFTree.set("name", fileN)
            for tag in self.getFileTagsL(fileN) :
                etree.SubElement(tagsFTree, "fileTag").text = tag
 
        # Save to XML file
        doc = etree.ElementTree(tagsAndFilesTree)
        doc.write(configN, encoding='utf-8', method="xml", pretty_print=True, xml_declaration=True) 
            
        self.log.info(HEADER, "Out writeConfig " + configN)


    def readTag(self, fileN) :
        self.log.info(HEADER, "In  readTag file=" + str(fileN))
        im = Image.open(fileN)
        attr = True
        try :
            imL = im.applist
        except :
            self.log.warn(HEADER, "In  readTag file="+str(fileN)+" has no tags")
            attr = False
        
        if attr :
            for segment, content in imL :
                try :
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
                                                tagN = levelLi.text
                                                if not self.tagDict.has_key(tagN) :
                                                    self.addSimpleTag(tagN, "True")
                                                self.addFileAndTags(fileN, tagN)
                except ValueError as err :
                    self.log.warn(HEADER, "In  readTag fileN"+str(fileN)+"\n  error="+str(err))


    def scanTags(self) :
        self.log.info(HEADER, "In  scanTags")
        self.fileDict = dict()
        if os.path.isdir(imagesDir) :
            for dirpath, dirnames, filenames in os.walk(imagesDir) :  # @UnusedVariable
                self.log.dbg("In  scanTags dirpath="+str(dirpath)+" dirnames="+str(dirnames)+" filenames="+str(filenames))
                if filenames.__len__ != 0 :
                    for filename in filenames :
                        extAuth=[".jpg", ".JPG", ".jpeg", ".JPEG", ".tif", ".TIF", ".gif", ".GIF", ".bmp", ".BMP"]
                        (fileN, extN) = os.path.splitext(filename)
                        if extAuth.__contains__(extN) :
                            fileWithPath = os.path.join(dirpath, filename)
                            self.readTag(fileWithPath)
        self.log.info(HEADER, "Out scanTags")


    def copyTags(self, tagsToCopy) :
        self.log.info(HEADER, "In  copyTags tagsToCopy=" + str(tagsToCopy))
        
        # Create link
        tagMulti = list()
        for sel in tagsToCopy :
            tagMulti.append([sel[0] + "/" + sel[1], sel[2]])
        self.log.dbg("In  copyTags tagMulti="+str(tagMulti))

        # Add it
        self.addMultiTag(tagMulti, True)

        self.log.info(HEADER, "Out copyTags")


    # With a tag name (included with + and -), 
    def delTags(self, tagsToDelete) :
        self.log.info(HEADER, "In  delTags tagsToDelete=" + str(tagsToDelete))
        for sel in tagsToDelete :
            foundElt = self.findElt(sel[0])
            if foundElt is not None :
                self.tagMultiList.remove(foundElt)
        self.log.info(HEADER, "Out delTags")


    def createLinks(self) :
        # delete link directory
        if os.path.isdir(linkDir) :
            shutil.rmtree(linkDir)
        os.makedirs(linkDir)

        i=0
        for fileN in self.getFiles() :
            #self.log.dbg("In  createLinks fileN="+str(fileN))
            tagsList = self.getFileTagsL(fileN)
            #self.log.dbg("In  createLinks tagsList="+str(tagsList))

            # filter with simple tags
            installSimple = False
            for tagN in tagsList :
                #self.log.dbg("In  createLinks tagN="+str(tagN)+"  en="+str(self.tagDict[tagN]))
                if self.tagDict[tagN] :
                    #self.log.dbg("In  createLinks installSimple tagN="+str(tagN)+"  en="+str(self.tagDict[tagN]))
                    installSimple = True
                else :
                    installSimple = False
                    break

            # filter with multiple tags
            matchFound = False
            installMulti = None
            #self.log.dbg("In  createLinks tagMultiList="+str(self.tagMultiList))
            for tagsEnM in self.tagMultiList :
                matchFoundOnce = False
                #self.log.dbg("In  createLinks tagsEnM="+str(tagsEnM))
                if tagsEnM[1] :
                    for tagM in tagsEnM[0] :
                        #self.log.dbg("In  createLinks tagM="+str(tagM))
                        # for enable, each tag must be present
                        if tagsList.__contains__(tagM[0]) :
                            #self.log.dbg("In  createLinks 1")
                            matchFoundOnce = True
                            if tagM[1] :
                                #self.log.dbg("In  createLinks 2")
                                if installMulti is None :
                                    installMulti = True
                            else :
                                #self.log.dbg("In  createLinks 3")
                                installMulti = False
                        else :
                            #self.log.dbg("In  createLinks 4")
                            matchFoundOnce = False
                            break

                if matchFoundOnce :
                    matchFound = True

            #self.log.dbg("In  createLinks matchFound="+str(matchFound))
            #self.log.dbg("In  createLinks installMulti="+str(installMulti))
            #self.log.dbg("In  createLinks installSimple="+str(installSimple))

            # installation priority
            install = False
            if matchFound :
                if installMulti :
                    install = True
            elif installSimple :
                install = True

            # installation
            #self.log.dbg("In  createLinks install="+str(install))
            if install :
                curDir = os.getcwd()
                os.chdir(linkDir)

                # create link name
                linkN = re.sub(homeDir, "", fileN)
                linkN = re.sub("/", "_", linkN)
                linkN = re.sub("^_", "", linkN)
                os.symlink(fileN, linkN)
                self.log.info(HEADER, "In  createLinks file="+str(fileN)+", link="+str(linkN))
                i += 1
        
                os.chdir(curDir)

        dialog_info("ScreenSaver Link", str(i) + " images ont été ajoutés.")








class GuiC(gtk.Window) :

    def __init__(self, logC) :
        self.log = logC
        self.simpleGuiC = TagGuiC(self, False, self.log)
        self.multiGuiC = TagGuiC(self, True, self.log)


    def run(self):
        self.log.info(HEADER, "In  run")

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
        except gobject.GError as err :
            self.log.warn(HEADER, "In  createWin progIcon="+str(progIcon)+"\n  error="+str(err))
        self.connect("destroy", self.on_destroy)

        self.set_title("Screensaver Images Tags")
        self.set_border_width(5)
        width = 1000
        height = 600
        self.set_size_request(width, height)


        #
        # Vertical box = tag lists + buttons
        #
        vTagBut = gtk.VBox(False, 5)
        #vTagBut.set_border_width(5)
        self.add(vTagBut)


        # Tag lists
        #

        # Horizontal box = tag list simple + buttons + multiple
        #
        hSimpleButMultiple = gtk.HBox(False, 5)
        hSimpleButMultiple.set_border_width(5)


        # Simple list
        #
        # Create the scrolled windows
        simpleTagSW = gtk.ScrolledWindow()
        simpleTagSW.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        simpleTagSW.set_shadow_type(gtk.SHADOW_IN)
        simpleTagSW.set_size_request(300, height-100)
        # Create tags treeview
        simpleTagSW.add(self.simpleGuiC.createTagTv())

        hSimpleButMultiple.pack_start(simpleTagSW, False, False)


        # Create buttons
        #
        tagButTab = gtk.Table(2, 1, False)
        #tagButTab.set_row_spacings(5)
        #tagButTab.set_col_spacings(5)

        # copy multiple selection
        gtk.stock_add([(gtk.STOCK_GO_FORWARD, "", 0, 0, "")])
        self.copyBut = gtk.Button(stock=gtk.STOCK_GO_FORWARD)
        self.copyBut.connect("clicked", self.onCopy)
        self.copyBut.set_sensitive(False)
        tagButTab.attach(self.copyBut, 0, 1, 0, 1, gtk.EXPAND, gtk.EXPAND, 10, 10)
        # remove multiple selection
        gtk.stock_add([(gtk.STOCK_GO_BACK, "", 0, 0, "")])
        self.delBut = gtk.Button(stock=gtk.STOCK_GO_BACK)
        self.delBut.connect("clicked", self.onDelete)
        self.delBut.set_sensitive(False)
        tagButTab.attach(self.delBut, 0, 1, 1, 2, gtk.EXPAND, gtk.EXPAND, 10, 10)

        hSimpleButMultiple.pack_start(tagButTab, False, False)


        # Multiple list
        #
        # Create the scrolled windows
        multiTagSW = gtk.ScrolledWindow()
        multiTagSW.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        multiTagSW.set_shadow_type(gtk.SHADOW_IN)
        #multiTagSW.set_size_request(width*3/5, height)
        # Create tags treeview
        # trick to copy 
        self.multiGuiC.tagC.tagMultiList = self.simpleGuiC.tagC.tagMultiList
        multiTagSW.add(self.multiGuiC.createTagTv())

        hSimpleButMultiple.pack_start(multiTagSW, True, True)

        vTagBut.add(hSimpleButMultiple)



        # Buttons
        #

        # Create buttons
        butTab = gtk.Table(1, 5, True)

        # scan tags
        gtk.stock_add([(gtk.STOCK_REFRESH, "Lire les tags", 0, 0, "")])
        scanBut = gtk.Button(stock=gtk.STOCK_REFRESH)
        scanBut.connect("clicked", self.onScan)
        butTab.attach(scanBut, 0, 1, 0, 1, gtk.EXPAND, gtk.EXPAND, 0, 0)
        # create links
        gtk.stock_add([(gtk.STOCK_EXECUTE, "Créé les images", 0, 0, "")])
        exeBut = gtk.Button(stock=gtk.STOCK_EXECUTE)
        exeBut.connect("clicked", self.onExecute)
        butTab.attach(exeBut, 1, 2, 0, 1, gtk.EXPAND, gtk.EXPAND, 0, 0)
        # quit
        quitBut = gtk.Button(stock=gtk.STOCK_QUIT)
        quitBut.connect("clicked", self.on_destroy)
        butTab.attach(quitBut, 4, 5, 0, 1, gtk.EXPAND, gtk.EXPAND, 0, 0)

        vTagBut.pack_start(butTab, False, False, 10)

        # Display the window
        self.show_all()

        self.log.info(HEADER, "Out createWin")


    def onCopy(self, button=None) :
        self.simpleGuiC.onCopyTags()
        # copy data
        self.multiGuiC.tagC.tagMultiList = self.simpleGuiC.tagC.tagMultiList
        #self.simpleGuiC.createModel()
        self.multiGuiC.createModel()


    def onDelete(self, button=None) :
        self.multiGuiC.onDelTags()
        self.multiGuiC.createModel()


    def onScan(self, button=None) :
        self.simpleGuiC.onScanTags()
        self.simpleGuiC.createModel()


    def onExecute(self, button=None) :
        # copy data
        self.simpleGuiC.tagC.tagMultiList = self.multiGuiC.tagC.tagMultiList
        self.simpleGuiC.onExeTags()







class TagGuiC(gtk.Window) :

    def __init__(self, parentW, multi, logC) :
        # window parameter
        self.mainWindow = parentW
        self.treeview = None

        self.log = logC
        self.tagC = TagC(self.log)
        self.model = self.initModel()
        self.multi = multi  # false = tag list left (single)
                            # true  = tag list right (multiple)

        self.memColEn = "current"
        self.memColEnMulti = "current"
        self.selMulti = list()  # [lvl1, lvl2, enable] (single)
                                # [tagName, tagEnable] (multiple)

        if not self.multi :
            self.tagC.readConfig()
            self.log.info(HEADER, "TagC = \n" + str(self.tagC))


    def initModel(self) :
        # create tree store
        return gtk.TreeStore(
                    gobject.TYPE_STRING,
                    gobject.TYPE_BOOLEAN,
                    gobject.TYPE_BOOLEAN,
                    gobject.TYPE_BOOLEAN)


    def createTagTv(self) :
        self.log.dbg("In  createTagTv")

        # create model
        self.createModel()

        # create tag treeview
        self.treeview = gtk.TreeView(self.model)
        self.treeview.set_rules_hint(True)
        self.treeview = self.addCol(self.treeview)
        self.treeview.expand_all()

        treeselect = self.treeview.get_selection()
        treeselect.set_mode(gtk.SELECTION_MULTIPLE)
        treeselect.connect('changed', self.onChanged)

        self.log.dbg("Out createTagTv")
        return self.treeview


    # Convert tag multi list to a special name (included with + and -)
    def convertListToSpecialName(self, listToConvert) :
        res = str()
        for pattern in listToConvert :
            if pattern[1] :
                res += "+ "
            else :
                res += "- "
            res += pattern[0] + " "
        res = re.sub(" $", "", res)
        return res


    def createModel(self) :
        self.log.info(HEADER, "In  createModel multi=" + str(self.multi))
        topLvl = list()
        self.model.clear()

        ## For multiple tags
        if self.multi :
            for tagsEnM in self.tagC.tagMultiList :
                tagLinfo = list()

                tagsName = self.convertListToSpecialName(tagsEnM[0])
                tagEn = tagsEnM[1]

                # name
                tagLinfo.append(tagsName)
                # enable
                tagLinfo.append(tagEn)
                # visible
                tagLinfo.append(True)
                # activatable
                tagLinfo.append(True)

                topLvl.append(tagLinfo)


        ## For simple tags
        else :
            # Construct list to put in model 
            tagsDict = self.tagC.getSimpleTagsByHier()
            tagsDictSort = tagsDict.keys()
            tagsDictSort.sort()
            for tag in tagsDictSort :
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

                # Add level 2
                lvl1L.append(lvl2L)

                topLvl.append(lvl1L)


        ## Add data to the tree store
        self.log.dbg("In  createModel topLvl="+str(topLvl))
        if topLvl :
            for tag in topLvl :
                tagIter = self.model.append(None)

                self.model.set(tagIter,
                    COL_NAME, tag[COL_NAME],
                    COL_ENABLE, tag[COL_ENABLE],
                    COL_ENABLE_VISIBLE, tag[COL_ENABLE_VISIBLE],
                    COL_ENABLE_ACTIVATABLE, tag[COL_ENABLE_ACTIVATABLE]
                )

                if not self.multi :
                    for lvl2 in tag[COL_CHILDREN] :
                        versionIter = self.model.append(tagIter)
                        self.model.set(versionIter,
                            COL_NAME, lvl2[COL_NAME],
                            COL_ENABLE, lvl2[COL_ENABLE],
                            COL_ENABLE_VISIBLE, lvl2[COL_ENABLE_VISIBLE],
                            COL_ENABLE_ACTIVATABLE, lvl2[COL_ENABLE_ACTIVATABLE]
                        )

        if self.treeview is not None :
            self.treeview.expand_all()

        self.log.info(HEADER, "Out createModel")


    def addCol(self, treeview) :
        self.log.dbg("In  addCol")
        model = treeview.get_model()

        # Column for tag's enable
        renderer = gtk.CellRendererToggle()
        renderer.set_property("xalign", 0.0)
        renderer.connect("toggled", self.onToggledItem, model)
        column = gtk.TreeViewColumn("Sélection", renderer, active=COL_ENABLE,
                                    visible=COL_ENABLE_VISIBLE, activatable=COL_ENABLE_ACTIVATABLE)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column.set_clickable(True)
        column.set_fixed_width(80)
        column.connect("clicked", self.onColEnable, model)

        treeview.append_column(column)

        # Column for tag's name
        renderer = gtk.CellRendererText()
        renderer.set_property("xalign", 0.0)
        column = gtk.TreeViewColumn("Nom des tags", renderer, text=COL_NAME)
        column.set_clickable(False)

        treeview.append_column(column)
        self.log.dbg("Out addCol")
        return treeview


    # When the user clicks on the column "enable"
    def onColEnable(self, cell, model) :
        if self.multi :
            self.log.info(HEADER, "In  onColEnable memColEnMulti=" + str(self.memColEnMulti))

            if self.memColEnMulti == "all" :
                self.memColEnMulti = "none"
            elif self.memColEnMulti == "none" :
                self.memColEnMulti = "current"
            elif self.memColEnMulti == "current" :
                self.memColEnMulti = "all"

            if self.memColEnMulti == "current" :
                self.tagC.readConfig()
            else :
                for tagsEnM in self.tagC.tagMultiList :
                    tagsName = self.convertListToSpecialName(tagsEnM[0])
                    if self.memColEnMulti == "all" :
                        self.tagC.setEnOnMulti(tagsName, True)
                    elif self.memColEnMulti == "none" :
                        self.tagC.setEnOnMulti(tagsName, False)

        else :
            self.log.info(HEADER, "In  onColEnable memColEn=" + str(self.memColEn))

            if self.memColEn == "all" :
                self.memColEn = "none"
            elif self.memColEn == "none" :
                self.memColEn = "current"
            elif self.memColEn == "current" :
                self.memColEn = "all"

            if self.memColEn == "current" :
                self.tagC.readConfig()
            else :
                for tagN in self.tagC.getSimpleTags() :
                    if self.memColEn == "all" :
                        self.tagC.setSimpleTagEn(tagN, True)
                    elif self.memColEn == "none" :
                        self.tagC.setSimpleTagEn(tagN, False)

        # update model
        self.createModel()

        self.log.info(HEADER, "Out onColEnable")


    # each time selection changes, this function is called
    def onChanged(self, selection) :
        self.log.info(HEADER, "In  onChanged")
        model, rows = selection.get_selected_rows()

        self.selMulti = list()
        for row in rows :
            iterSel = model.get_iter(row)
            
            if self.multi :
                selName = model.get_value(iterSel, COL_NAME)
                selEn = model.get_value(iterSel, COL_ENABLE)
                self.selMulti.append([selName.decode('utf-8'), selEn])

                if self.selMulti.__len__() > 0 :
                    self.mainWindow.delBut.set_sensitive(True)
                else :
                    self.mainWindow.delBut.set_sensitive(False)

            else :
                iterSel_has_child = model.iter_has_child(iterSel)

                if iterSel_has_child :
                    selLvl1 = model.get_value(iterSel, COL_NAME)
                    selLvl2 = None
                    selEn = False
                elif not iterSel_has_child :
                    iterSelParent = model.iter_parent(iterSel)
                    selLvl1 = model.get_value(iterSelParent, COL_NAME)
                    selLvl2 = model.get_value(iterSel, COL_NAME)
                    selEn = model.get_value(iterSel, COL_ENABLE)
                    self.selMulti.append([selLvl1.decode('utf-8'), selLvl2.decode('utf-8'), selEn])
        
                if self.selMulti.__len__() > 1 :
                    self.mainWindow.copyBut.set_sensitive(True)
                else :
                    self.mainWindow.copyBut.set_sensitive(False)

        self.log.info(HEADER, "Out onChanged selMulti=" + str(self.selMulti))


    # When user clicks on a box
    def onToggledItem(self, cell, path_str, model) :
        self.log.info(HEADER, "In  onToggledItem")

        iterSel = model.get_iter_from_string(path_str)
        
        if self.multi :
            # Get name
            selName = model.get_value(iterSel, COL_NAME)
            # Get enable (before click)
            selEnable = model.get_value(iterSel, COL_ENABLE)

            self.log.dbg("selName=" + str(selName))
            self.log.dbg("selEnable=" + str(selEnable))

            # Disable
            # From True to False (as value is before clicking)
            if selEnable :
                self.tagC.setEnOnMulti(selName.decode('utf-8'), False)
                model.set(iterSel, COL_ENABLE, False)

            # Enable
            # From False to True
            else :
                self.tagC.setEnOnMulti(selName.decode('utf-8'), True)
                model.set(iterSel, COL_ENABLE, True)

        else :
            # Get enable (before click)
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
                self.tagC.setSimpleTagEn(selTagN.decode('utf-8'), False)
                model.set(iterSel, COL_ENABLE, False)

            # Enable
            # From False to True
            else :
                self.tagC.setSimpleTagEn(selTagN.decode('utf-8'), True)
                model.set(iterSel, COL_ENABLE, True)

        self.log.info(HEADER, "Out onToggledItem")


    # Create multiple tags
    def onCopyTags(self) :
        self.tagC.copyTags(self.selMulti)


    # Delete multiple tags
    def onDelTags(self) :
        self.tagC.delTags(self.selMulti)


    # Create multiple tags
    def onScanTags(self) :
        self.tagC.scanTags()


    # Create links
    def onExeTags(self) :
        self.tagC.writeConfig()
        self.tagC.createLinks()


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

