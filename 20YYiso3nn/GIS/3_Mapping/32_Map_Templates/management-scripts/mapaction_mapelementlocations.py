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
import sys
import string
import shutil
from shutil import copyfile
import datetime
today = str(datetime.datetime.now())

sep = os.path.sep

# gets location of this python script which is at root of github
rootauto = os.getcwd()
mapfile = rootauto + sep + "template_positions_" + today[0:10] + ".txt"

# setting up are workspace
arcpy.env.workspace = rootauto[:-19]
# lists all the mxd's in the relevant folder
mxdList = arcpy.ListFiles("*.mxd")
# final 'element' variable
element_final = ''

# loop through the elements and record the values
header = "MapName,Type,ElementName,PositionX,PositionY,Height,Width,FontSize,TextValue"

for mxdfile in mxdList:
    mxd = arcpy.mapping.MapDocument(rootauto[:-19] + sep + mxdfile)
    elemmxd = mxdfile
    element = ""
    df = arcpy.mapping.ListDataFrames(mxd, "*")
    # run through the elements within the map and print
    for elem in arcpy.mapping.ListLayoutElements(mxd, ""):
    # just printing to the screen
        elemname = str(elem.name)
        elemtype = str(elem.type)
        elemposx = str(elem.elementPositionX)
        elemposy = str(elem.elementPositionY)
        elemheight = str(elem.elementHeight)
        elemwidth = str(elem.elementWidth)
        element = element + "\n"+ elemmxd + "," + elemname + "," + elemtype + ","
        element = element + elemposx + "," + elemposy + "," + elemheight + "," + elemwidth    

        if elemtype == "TEXT_ELEMENT":
            elemfontsize = str(elem.fontSize)
            elemtext = str(elem.text)
            element = element + "," + elemfontsize + "," + elemtext

    element = element
    # in case of unicode
    element = str(element)
    # convert to List and order alphabetically
    testLst = element.split("\n")
    # avoid treatment of capital letters as lower values when ordering alphabetically
    testLst.sort(key=str.lower)

    # Create alphabetic element
    element_alphabetic = "\n".join(testLst)
    element_final = element_final + element_alphabetic + "\n"

    # Saving 10.1, 10.0 and 9.3 copies of mxd's in correct location and name
    mxd10_1 = rootauto[:-19] + sep + "previous_versions" + sep + "arcmap_10_1" + sep + mxdfile[:7] + "10_1" + mxdfile[11:]
    mxd.saveACopy(mxd10_1, "10.1")
    mxd10_0 = rootauto[:-19] + sep + "previous_versions" + sep + "arcmap_10_0" + sep + mxdfile[:7] + "10_0" + mxdfile[11:]
    mxd.saveACopy(mxd10_0, "10.0")
    mxd9_3 = rootauto[:-19] + sep + "previous_versions" + sep + "arcmap_9_3" + sep + mxdfile[:7] + "9_3" + mxdfile[11:]
    mxd.saveACopy(mxd9_3, "9.3")

    finaljpg = rootauto[:-19] + sep + "example-outputs" + sep + mxdfile[:-4] + ".jpg"
    print finaljpg
    os.remove(finaljpg)
    arcpy.mapping.ExportToJPEG(mxd, finaljpg, resolution = 300)

# open template_positions_yyyymmdd.txt
file_object = open(mapfile, "w+")
# add 'header' variable to file
element_final = header + element_final
file_object.write(element_final)
file_object.close()
