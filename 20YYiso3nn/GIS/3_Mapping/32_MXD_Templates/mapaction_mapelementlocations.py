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
# Setting up variables
##root = rootauto + r"\default-crash-move-folder\20YYiso3nn\GIS\3_Mapping\32_MXD_Templates\arcgis_10_6"
root = rootauto + r"\arcgis_10_6"

# setting the workspace for the arcpy calls
arcpy.env.workspace = root
# lists all the mxd's in the relevant folder
mxdList = arcpy.ListFiles("*.mxd")
    
# loop through the elements and re5cord the values
print "Template,Element,PositionX,PositionY,Height,Width"
##mapframedetails = []
for mxdfile in mxdList:
##    mapframedetails.append(mxdfile)
    mxd = arcpy.mapping.MapDocument(root + sep + mxdfile)
    df = arcpy.mapping.ListDataFrames(mxd, "*")
    # run through the elements within the map and print
    for elem in arcpy.mapping.ListLayoutElements(mxd, ""):
        print str(mxdfile) + ",",
        print str(elem.name) + ",",
##        print str(elem.textSize) + ",",
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

    # want to generate a list / array which can be sorted alphabetically
    # help please
##        element = element +  mapfile + ","
##        element = element +  str(elem.name) + ",",
##        element = element +  str(elem.elementPositionX) + "\n"#",",
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
