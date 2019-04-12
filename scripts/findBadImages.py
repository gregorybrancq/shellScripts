#!/usr/bin/env python


import os
from PIL import Image

fileImgList = list()
badFiles = list()
imgDir = "/home/greg/Images"
#imgDir = "/home/greg/test"

#fileImgList = [ f for f in os.listdir(imgDir) if (os.path.isfile(os.path.join(imgDir,f))) ]
#fileImgList = glob.glob(imgDir)
for dirpath, dirnames, files in os.walk(imgDir) :
    for f in files :
        fileImgList.append(os.path.join(dirpath, f))
#print str(fileImgList)
print "Nbre files = " + str(fileImgList.__len__()) + "\n"

for f in fileImgList :
    try :
        img=Image.open(f)
        img.load()
    except IOError :
        badFiles.append(f)

print "Bad files = " + str(badFiles.__len__()) + "\n"
for badFile in badFiles :
    print str(badFile)
