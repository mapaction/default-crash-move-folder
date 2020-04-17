""" This scripts brings together all data and maps for the report """

import sys
sys.path.append("C:\\py27arcgis106\\ArcGIS10.6\\Lib\\site-packages")
sys.path.append(r'C:\Program Files (x86)\ArcGIS\Desktop10.6\arcpy')
sys.path.append(r'C:\Program Files (x86)\ArcGIS\Desktop10.6\ArcToolbox\Scripts')
sys.path.append(r'C:\Program Files (x86)\ArcGIS\Desktop10.6\bin')
sys.path.append("C:\\py27arcgis106\\ArcGIS10.6\\Lib")
import arcpy
from arcpy import env

import os
import string
import shutil
from shutil import copyfile

import os
sep = os.path.sep

# gets location of this python script which is at root of github
rootauto = os.path.abspath(os.getcwd())
# Setting up variables
root = rootauto + r"\arcgis_10_6"

# setting the workspace for the arcpy calls
arcpy.env.workspace = root
# lists all the mxd's in the relevant folder
mxdList = arcpy.ListFiles("*.mxd")
    
# loop through the elements and re5cord the values
print "Template,Element,PositionX,PositionY,Height,Width"
for mxdfile in mxdList:
    mxd = arcpy.mapping.MapDocument(root + sep + mxdfile)
    df = arcpy.mapping.ListDataFrames(mxd, "*")
    # run through the elements within the map and print
    for elem in arcpy.mapping.ListLayoutElements(mxd, ""):
        print str(mxdfile) + ",",
        print str(elem.name) + ",",
        print str(elem.elementPositionX) + ",",
        print str(elem.elementPositionY) + ",",
        print str(elem.elementHeight) + ",",
        print str(elem.elementWidth)
    print "\n"

    # Saving 10.2 and 9.3 copies of mxd's in correct location and name
    mxd10_1 = root[:-4] + "10_2" + sep + mxdfile[:7] + "10_2" + mxdfile[11:]
    mxd.saveACopy(mxd10_1, "10.1")
    mxd9_3 = root[:-4] + "9_3" + sep + mxdfile[:7] + "9_3" + mxdfile[11:]
    mxd.saveACopy(mxd9_3, "9.3")
