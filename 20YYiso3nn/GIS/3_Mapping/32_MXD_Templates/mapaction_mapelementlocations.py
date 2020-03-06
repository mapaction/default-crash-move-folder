""" This scripts brings together all data and maps for the report """
import os
import string
import shutil
from shutil import copyfile
import arcpy
from arcpy import env

import os
rootauto = os.path.abspath(os.getcwd())
##rootauto = os.path.dirname(os.path.abspath(__mapaction_mapelementlocations.py__))
print rootauto
# Setting up variables
##root = "C:/ff_GitHub/default-crash-move-folder/20YYiso3nn/GIS/3_Mapping/32_MXD_Templates/arcgis_10_6/"
##arcpy.env.workspace = root
##mxdList = arcpy.ListFiles("*.mxd")
##
### loop through the elements and re5cord the values
##print "Template,Element,PositionX,PositionY,Height,Width"
##mapframedetails = []
##for mxdfile in mxdList:
##    mapframedetails.append(mxdfile)
##    mxd = arcpy.mapping.MapDocument(root + mxdfile)
##    df = arcpy.mapping.ListDataFrames(mxd, "*")
##    for elem in arcpy.mapping.ListLayoutElements(mxd, ""):
##        print str(mxdfile) + ",",
##        print str(elem.name) + ",",
####        print str(elem.textSize) + ",",
##        print str(elem.elementPositionX) + ",",
##        print str(elem.elementPositionY) + ",",
##        print str(elem.elementHeight) + ",",
##        print str(elem.elementWidth)
##    print "\n"
##
####        mapframedetails.append(elem.name)
####        mapframedetails.append(",")
####        mapframedetails.append(elem.elementHeight)
####        mapframedetails.append(",")
####        mapframedetails.append(elem.elementWidth)
####        mapframedetails.append(",")
####        mapframedetails.append(elem.elementPositionX)
####        mapframedetails.append(",")
####        mapframedetails.append(elem.elementPositionY)
####        mapframedetails.append("\n")
####    print mapframedetails
####    print "\n"
