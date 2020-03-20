#!/usr/bin/env python
# coding: utf-8

'''
tagImages

program to set EXIF tag on images.
'''




###############################################
# Imports
###############################################

# use for graphical interface
import sys
import os
import re
import time
from optparse import OptionParser
import xml.etree.ElementTree as ET
from PIL.ExifTags import TAGS
from PIL import Image
import warnings
# To avoid kind of warnings
# /usr/lib/python2.7/dist-packages/PIL/Image.py:2514: DecompressionBombWarning: Image size (131208140 pixels) exceeds limit of 89478485 pixels, could be decompression bomb DOS attack.
warnings.simplefilter('ignore', Image.DecompressionBombWarning)

## common
from python_common import *
HEADER = "tagImages"

## directory
homeDir = getHomeDir()
logDir  = getLogDir()

###############################################



###############################################
## Global variables
###############################################

t = str(datetime.today().isoformat("_"))
logFile = os.path.join(logDir, HEADER + "_" + t + ".log")

# Minimum parameters for each image to be installed
minWidth  = 800
minHeight = 800

fileImgList = list()
badFiles = list()

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
    "--dir",
    action  = "store",
    dest    = "directory",
    default = "/home/greg/Images",
    help    = "Specify the directory."
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

###############################################



###############################################
###############################################
##                FUNCTIONS                  ##
###############################################
###############################################

# #fileImgList = [ f for f in os.listdir(parsedArgs.directory) if (os.path.isfile(os.path.join(parsedArgs.directory,f))) ]
# #fileImgList = glob.glob(parsedArgs.directory)
# for dirpath, dirnames, files in os.walk(parsedArgs.directory) :
#     for f in files :
#         fileImgList.append(os.path.join(dirpath, f))
# #print str(fileImgList)
# print "Nbre files = " + str(fileImgList.__len__()) + "\n"
# 
# for f in fileImgList :
#     try :
#         img=Image.open(f)
#         img.load()
#         exif_data = img._getexif()
#         #print f, exif_data
#     except IOError :
#         badFiles.append(f)
# 
# for f in fileImgList :
#     im = Image.open(f)
#     attr = True
#     try :
#         imL = im.applist
#     except :
#         log.warn(HEADER, "In  readTag file="+str(f)+" has no tags")
#         attr = False
#     
#     good = True
#     (width, height) = im.size
#     if (width < minWidth) or (height < minHeight) :
#         log.warn(HEADER, "In  readTag size of file="+str(f)+" is too small (width = " + str(width) + ", height = " + str(height)+ ").")
#         good = False
# 
#     if attr and good :
#         for segment, content in imL :
#             try :
#                 marker, body = content.split('\x00', 1)
#                 if segment == 'APP1' and marker == 'http://ns.adobe.com/xap/1.0/' :
#                     root = ET.fromstring(body)
# 
#                     for levelRDF in root :
#                         #print "LevelRDF=" + levelRDF.tag
#                         for levelDescription in levelRDF :
#                             #print "levelDescription.tag=" + levelDescription.tag
#                             for levelTagsList in levelDescription :
#                                 #print "levelTagsList.tag=" + levelTagsList.tag
#                                 if levelTagsList.tag == "{http://www.digikam.org/ns/1.0/}TagsList" :
#                                     for levelSeq in levelTagsList :
#                                         print "levelSeq.tag=" + levelSeq.tag
#                                         for levelLi in levelSeq :
#                                             tagN = levelLi.text
#                                             print (f, tagN)
#                                             #if not self.tagDict.has_key(tagN) :
#                                             #    self.addSimpleTag(tagN, "True")
#                                             #self.addFileAndTags(f, tagN)
#             except ValueError as err :
#                 log.warn(HEADER, "In  readTag fileN"+str(fileN)+"\n  error="+str(err))


im = Image.open("IMG_6371.JPG")
attr = True
try :
    imL = im.applist
except :
    log.warn(HEADER, "In  readTag file="+str(f)+" has no tags")
    attr = False

if attr :
    for segment, content in imL :
        try :
            print segment, content, "\n"
            marker, body = content.split('\x00', 1)
            if segment == 'APP1' and marker == 'http://ns.adobe.com/xap/1.0/' :
                root = ET.fromstring(body)

                for levelRDF in root :
                    #print "LevelRDF=" + levelRDF.tag
                    for levelDescription in levelRDF :
                        #print "levelDescription.tag=" + levelDescription.tag
                        for levelTagsList in levelDescription :
                            print "levelTagsList=" + str(levelTagsList)
                            print "levelTagsList.tag=" + str(levelTagsList.tag)
                            print "levelTagsList.items=" + str(levelTagsList.items)
                            print "levelTagsList.keys=" + str(levelTagsList.keys)
                            if levelTagsList.tag == "{http://www.digikam.org/ns/1.0/}TagsList" :
                                levelSeqOld = levelTagsList.copy()
                                #help(levelTagsList)
                                #levelTagsList.add("Personne/Tilou")
                            
                                print "GBR old = " + str(levelSeqOld)
                                #print "GBR new = " + str(levelSeq)

                                for levelSeq in levelTagsList :
                                    print "levelSeq=" + str(levelSeq)
                                    print "levelSeq.tag=" + str(levelSeq.tag)
                                    #help(levelSeq)
                                    print "BEFORE"
                                    for levelLi in levelSeq :
                                        tagN = levelLi.text
                                        print (tagN)
                                        #if not self.tagDict.has_key(tagN) :
                                        #    self.addSimpleTag(tagN, "True")
                                        #self.addFileAndTags(f, tagN)
                                    levelSeq.insert(0, "Personne/Tilou")
        except ValueError as err :
            log.warn(HEADER, "In  readTag fileN"+str(fileN)+"\n  error="+str(err))

im.save("IMG_6371_BIS.JPG")
im.close()

time.sleep(2)
print "AFTER"

im = Image.open("IMG_6371_BIS.JPG")
attr = True
try :
    imL = im.applist
except :
    log.warn(HEADER, "In  readTag file="+str(f)+" has no tags")
    attr = False

if attr :
    for segment, content in imL :
        try :
            marker, body = content.split('\x00', 1)
            if segment == 'APP1' and marker == 'http://ns.adobe.com/xap/1.0/' :
                root = ET.fromstring(body)

                for levelRDF in root :
                    print "LevelRDF=" + levelRDF.tag
                    for levelDescription in levelRDF :
                        #print "levelDescription.tag=" + levelDescription.tag
                        for levelTagsList in levelDescription :
                            if levelTagsList.tag == "{http://www.digikam.org/ns/1.0/}TagsList" :
                                for levelSeq in levelTagsList :
                                    for levelLi in levelSeq :
                                        tagN = levelLi.text
                                        print (tagN)
        except ValueError as err :
            log.warn(HEADER, "In  readTag fileN"+str(fileN)+"\n  error="+str(err))


#print "Bad files = " + str(badFiles.__len__()) + "\n"
#for badFile in badFiles :
#    print str(badFile)

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
    log = LOGC(logFile, HEADER, parsedArgs.debug)



if __name__ == '__main__':
    main()

###############################################






APP1 http://ns.adobe.com/xap/1.0/
<?xpacket begin="﻿" id="W5M0MpCehiHzreSzNTczkc9d"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="XMP Core 4.4.0-Exiv2">
    <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
        <rdf:Description rdf:about="" xmlns:xmp="http://ns.adobe.com/xap/1.0/" xmlns:tiff="http://ns.adobe.com/tiff/1.0/" xmlns:digiKam="http://www.digikam.org/ns/1.0/" xmlns:MicrosoftPhoto="http://ns.microsoft.com/photo/1.0/" xmlns:lr="http://ns.adobe.com/lightroom/1.0/" xmlns:mediapro="http://ns.iview-multimedia.com/mediapro/1.0/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:acdsee="http://ns.acdsee.com/iptc/1.0/" xmp:Rating="0" xmp:CreatorTool="digiKam-5.6.0" tiff:Software="digiKam-5.6.0" acdsee:categories="&lt;Categories&gt;&lt;Category Assigned=&quot;0&quot;&gt;Personne&lt;Category Assigned=&quot;1&quot;&gt;Juju&lt;/Category&gt;&lt;Category Assigned=&quot;1&quot;&gt;Gabriël&lt;/Category&gt;&lt;Category Assigned=&quot;1&quot;&gt;Bertrand&lt;/Category&gt;&lt;Category Assigned=&quot;1&quot;&gt;Diane&lt;/Category&gt;&lt;Category Assigned=&quot;1&quot;&gt;Tom&lt;/Category&gt;&lt;Category Assigned=&quot;1&quot;&gt;Laëtitia&lt;/Category&gt;&lt;Category Assigned=&quot;1&quot;&gt;Lilou&lt;/Category&gt;&lt;Category Assigned=&quot;1&quot;&gt;Hugo&lt;/Catcréer un média de récupération avec HP Recovery Manager.egory&gt;&lt;Category Assigned=&quot;1&quot;&gt;Greg&lt;/Category&gt;&lt;Category Assigned=&quot;1&quot;&gt;Roseline&lt;/Category&gt;&lt;Category Assigned=&quot;1&quot;&gt;Rachel&lt;/Category&gt;&lt;Category Assigned=&quot;1&quot;&gt;Hanna&lt;/Category&gt;&lt;Category Assigned=&quot;1&quot;&gt;PM&lt;/Category&gt;&lt;/Category&gt;&lt;Category Assigned=&quot;0&quot;&gt;Année&lt;Category Assigned=&quot;1&quot;&gt;2019&lt;/Category&gt;&lt;/Category&gt;&lt;Category Assigned=&quot;0&quot;&gt;Lieu&lt;Category Assigned=&quot;1&quot;&gt;Vaudreuil&lt;/Category&gt;&lt;/Category&gt;&lt;/Categories&gt;"> 
            <digiKam:TagsList> 
                <rdf:Seq> <rdf:li>Personne/PM</rdf:li> <rdf:li>Personne/Hanna</rdf:li> <rdf:li>Personne/Rachel</rdf:li> <rdf:li>Personne/Roseline</rdf:li> <rdf:li>Personne/Greg</rdf:li> <rdf:li>Personne/Hugo</rdf:li> <rdf:li>Personne/Lilou</rdf:li> <rdf:li>Personne/Laëtitia</rdf:li> <rdf:li>Personne/Tom</rdf:li> <rdf:li>Année/2019</rdf:li> <rdf:li>Personne/Diane</rdf:li> <rdf:li>Personne/Bertrand</rdf:li> <rdf:li>Lieu/Vaudreuil</rdf:li> <rdf:li>Personne/Gabriël</rdf:li> <rdf:li>Personne/Juju</rdf:li> </rdf:Seq>
            </digiKam:TagsList>
            <MicrosoftPhoto:LastKeywordXMP> <rdf:Bag> <rdf:li>Personne/PM</rdf:li> <rdf:li>Personne/Hanna</rdf:li> <rdf:li>Personne/Rachel</rdf:li> <rdf:li>Personne/Roseline</rdf:li> <rdf:li>Personne/Greg</rdf:li> <rdf:li>Personne/Hugo</rdf:li> <rdf:li>Personne/Lilou</rdf:li> <rdf:li>Personne/Laëtitia</rdf:li> <rdf:li>Personne/Tom</rdf:li> <rdf:li>Année/2019</rdf:li> <rdf:li>Personne/Diane</rdf:li> <rdf:li>Personne/Bertrand</rdf:li> <rdf:li>Lieu/Vaudreuil</rdf:li> <rdf:li>Personne/Gabriël</rdf:li> <rdf:li>Personne/Juju</rdf:li> </rdf:Bag> 
            </MicrosoftPhoto:LastKeywordXMP>
            <lr:hierarchicalSubject> <rdf:Bag> <rdf:li>Personne|PM</rdf:li> <rdf:li>Personne|Hanna</rdf:li> <rdf:li>Personne|Rachel</rdf:li> <rdf:li>Personne|Roseline</rdf:li> <rdf:li>Personne|Greg</rdf:li> <rdf:li>Personne|Hugo</rdf:li> <rdf:li>Personne|Lilou</rdf:li> <rdf:li>Personne|Laëtitia</rdf:li> <rdf:li>Personne|Tom</rdf:li> <rdf:li>Année|2019</rdf:li> <rdf:li>Personne|Diane</rdf:li> <rdf:li>Personne|Bertrand</rdf:li> <rdf:li>Lieu|Vaudreuil</rdf:li> <rdf:li>Personne|Gabriël</rdf:li> <rdf:li>Personne|Juju</rdf:li> </rdf:Bag> 
            </lr:hierarchicalSubject>
            <mediapro:CatalogSets> <rdf:Bag> <rdf:li>Personne|PM</rdf:li> <rdf:li>Personne|Hanna</rdf:li> <rdf:li>Personne|Rachel</rdf:li> <rdf:li>Personne|Roseline</rdf:li> <rdf:li>Personne|Greg</rdf:li> <rdf:li>Personne|Hugo</rdf:li> <rdf:li>Personne|Lilou</rdf:li> <rdf:li>Personne|Laëtitia</rdf:li> <rdf:li>Personne|Tom</rdf:li> <rdf:li>Année|2019</rdf:li> <rdf:li>Personne|Diane</rdf:li> <rdf:li>Personne|Bertrand</rdf:li> <rdf:li>Lieu|Vaudreuil</rdf:li> <rdf:li>Personne|Gabriël</rdf:li> <rdf:li>Personne|Juju</rdf:li> </rdf:Bag> 
            </mediapro:CatalogSets>
            <dc:subject> <rdf:Bag> <rdf:li>PM</rdf:li> <rdf:li>Hanna</rdf:li> <rdf:li>Rachel</rdf:li> <rdf:li>Roseline</rdf:li> <rdf:li>Greg</rdf:li> <rdf:li>Hugo</rdf:li> <rdf:li>Lilou</rdf:li> <rdf:li>Laëtitia</rdf:li> <rdf:li>Tom</rdf:li> <rdf:li>2019</rdf:li> <rdf:li>Diane</rdf:li> <rdf:li>Bertrand</rdf:li> <rdf:li>Vaudreuil</rdf:li> <rdf:li>Gabriël</rdf:li> <rdf:li>Juju</rdf:li> </rdf:Bag> 
            </dc:subject> 
        </rdf:Description> 
    </rdf:RDF> 
</x:xmpmeta>
