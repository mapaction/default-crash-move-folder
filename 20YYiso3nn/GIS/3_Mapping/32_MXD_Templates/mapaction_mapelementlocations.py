""" This scripts brings together all data and maps for the report """
import os
import string
import shutil
from shutil import copyfile
import arcpy
from arcpy import env

# Setting up variables
root = "C:/ff_GitHub/default-crash-move-folder/20YYiso3nn/GIS/3_Mapping/32_MXD_Templates/arcgis_10_6/"
arcpy.env.workspace = root
mxdList = arcpy.ListFiles("*.mxd")

# loop through the elements and re5cord the values
mapframedetails = []
for mxdfile in mxdList:
    mapframedetails.append(mxdfile)
    print mxdfile
    print "element,position x,position y,height,width"
    mxd = arcpy.mapping.MapDocument(root + mxdfile)
    df = arcpy.mapping.ListDataFrames(mxd, "*")
    for elem in arcpy.mapping.ListLayoutElements(mxd, ""):
        print str(elem.name) + ",",
        print str(elem.elementPositionX) + ",",
        print str(elem.elementPositionY) + ",",
        print str(elem.elementHeight) + ",",
        print str(elem.elementWidth)
    print "\n"

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
##    print mapframedetails
##    print "\n"
