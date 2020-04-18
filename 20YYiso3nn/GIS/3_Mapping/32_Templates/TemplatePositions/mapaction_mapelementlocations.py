""" This scripts brings together all data and maps for the report """
import os
import string
import shutil
from shutil import copyfile
import arcpy
from arcpy import env

import os
sep = os.path.sep

# gets location of this python script which is at root of github
rootauto = os.path.abspath(os.getcwd())
print rootauto
# Setting up variables
mainroot = rootauto + r"\MapAction_Darren\default-crash-move-folder"
root = mainroot + "\20YYiso3nn\GIS\3_Mapping\32_MXD_Templates\arcgis_10_6"
##root = r"C:\AutoTest\CMF\GIS\3_Mapping\32_MXD_Templates\arcgis_10_6"
print root
arcpy.env.workspace = root
# lists all the mxd's in the relevant folder
mxdList = arcpy.ListFiles("*.mxd")
    
# loop through the elements and re5cord the values
print "Template,Type,ElementName,PositionX,PositionY,Height,Width,FontSize,TextValue"
##mapframedetails = []
for mxdfile in mxdList:
    print mxdfile
##    mapframedetails.append(mxdfile)
    mxd = arcpy.mapping.MapDocument(root + sep + mxdfile)
    df = arcpy.mapping.ListDataFrames(mxd, "*")
    for elem in arcpy.mapping.ListLayoutElements(mxd, ""):
        print str(mxdfile) + ",",
        print str(elem.name) + ",",
        print str(elem.type) + ",",
        print str(elem.elementPositionX) + ",",
        print str(elem.elementPositionY) + ",",
        print str(elem.elementHeight) + ",",
        print str(elem.elementWidth) + ",",
        if str(elem.type) == "TEXT_ELEMENT":
            print str(elem.fontSize) + ",",
            print str(elem.text)
    print "\n"

    # Saving 10.2 and 9.3 copies of mxd's in correct location and name
    mxd10_1 = root[:-4] + "10_2" + sep + mxdfile[:7] + "10_2" + mxdfile[11:]
    mxd.saveACopy(mxd10_1, "10.1")
    mxd9_3 = root[:-4] + "9_3" + sep + mxdfile[:7] + "9_3" + mxdfile[11:]
    mxd.saveACopy(mxd9_3, "9.3")

##        mapfile = str(mxdfile[0]) + ",",
##        print mapfile
##        name = str(elem.name) + ",",
##        positionY = str(elem.elementPositionY) + ",",
##        height = str(elem.elementHeight) + ",",
##        width = str(elem.elementWidth)
##
##        element = mapfile + ","
##        element = name + ",",
##        element = positionX + "\n"#",",
##        element = element +  str(elem.elementPositionY) + ",",
##        element = element +  str(elem.elementHeight) + ",",
##        element = element +  str(elem.elementWidth) + "\n"
        
##        mapframedetails.append(element)
##        mapframedetails.append(",")
##        mapframedetails.append(elem.name)
##        mapframedetails.append(",")
##        mapframedetails.append(elem.elementHeight)
##        mapframedetails.append(",")
##        mapframedetails.append(elem.elementWidth)
##        mapframedetails.append(",")
##        mapframedetails.append(elem.elementPositionX)
##        mapframedetails.append(",")
##        mapframedetails.append(elem.elementPositionY)
##        mapframedetails.append("\n")
##    mapframedetails.sort()
##    print mapframedetails
##    print "\n"
