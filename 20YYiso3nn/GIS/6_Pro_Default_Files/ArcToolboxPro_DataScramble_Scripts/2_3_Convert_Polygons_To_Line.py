# -*- coding: utf-8 -*-
"""==============================================================================
  
Title          :2_3_Convert_Polygons_To_Line.py
Description    :Convert polygon to lines and remove all overlapping lines - MA linework
Author         :Tom H, Darren C and LF Velasquez
Date           :2023-09-14
Version        :1.0
Usage          :Inside ArcPro as part of the MapAction_Data_Scramble_2023.atbx
Notes          :This script must be run as part of the MapAction_Data_Scramble_2023.atbx
                in ArcPro, as otherwise it will return an error as part of the user input
python version  :3.9.16 as per ArcPro 3.1 sys.version
 
=============================================================================="""

# =============================================================================
# Modules - Libraries
# =============================================================================

import os,sys
import arcpy
from pathlib import Path

# =============================================================================
# Settign the ArcPro environment
# =============================================================================

# Set the script in the current ArcPro project
aprx = arcpy.mp.ArcGISProject("CURRENT")

# Set the right map or layout
# This is where the user is running the tool
frame_name = aprx.activeMap.name
mframe = aprx.listLayouts(frame_name)
arcpy.AddMessage(' MapFrame is {}'.format(frame_name))


arcpy.env.overwriteOutput = True
sep = os.path.sep
stars = "**********************"

# Set the outputMFlag environment to Disabled
arcpy.env.outputMFlag = "Disabled"
# Set the outputZFlag environment to Disabled
arcpy.env.outputZFlag = "Disabled"

# =============================================================================
# Process
# =============================================================================

try:
    
    # Ask for inputs inside ArcPro
    # This need setting insidde the toolbox script properties
    cmf = Path(arcpy.GetParameterAsText(0))
    arcpy.AddMessage(stars)
    arcpy.AddMessage(f'The cmf is {cmf}')

    # Set the field and geodatabase names
    gdbName = "tempGDB.gdb"

    # Defining the right path were the files need to be at the end
    gdbfldr = "202_admn" + sep + gdbName
    gdbPath = str(Path(cmf / gdbfldr))
    arcpy.AddMessage(gdbPath)

    # Delete then create working geoDatabase
    if arcpy.Exists(gdbPath):
        arcpy.Delete_management(gdbPath)
    arcpy.CreateFileGDB_management(str(Path(cmf / gdbfldr).parent), gdbName)

    # Move shp to gdb
    arcpy.env.workspace = str(Path(cmf / "202_admn"))
    fcList = arcpy.ListFeatureClasses("*py*")
    for polyAdmin in fcList:
        polyAdmin_loc = str(Path(cmf / f'202_admn\{polyAdmin}'))
        
        arcpy.AddMessage(stars)
        # Repair the geometry of the polyAdmin's in the gdb
        arcpy.AddMessage("Repairing the geometry of the polyAdmin's in the gdb")
        arcpy.RepairGeometry_management(polyAdmin)
        
        # Find the location of this string as used to rebuild the ln polyAdmin
        # Use string replace py -> ln
        lineAdmin = str (Path(cmf / f'202_admn\{gdbName}\{polyAdmin.replace("_py_", "_ln_")}'))
        
        # Add line feature class to gdb
        arcpy.AddMessage(stars)
        arcpy.AddMessage("Converting py to ln inside gdb")
        if arcpy.Exists(lineAdmin):
            arcpy.Delete_management(lineAdmin)
            
        arcpy.PolygonToLine_management(polyAdmin_loc, lineAdmin[:-4], "IDENTIFY_NEIGHBORS")
        arcpy.AddMessage(f' Converted polygon to line {lineAdmin[:-4]}')
        arcpy.AddMessage(' ')


    ## Deleting duplicate linework
    arcpy.AddMessage(stars)
    arcpy.AddMessage(' Deleting line work which is coincident with higher level admin')
        
    # Create list of unique sc names for ln data only
    arcpy.env.workspace = gdbPath
    dataLine = arcpy.ListFeatureClasses(feature_type = 'Line')
    arraySrc = []
    arrayModify = []
    for dataFCs in sorted(dataLine):
        arraySrc.append(dataFCs.split('_')[5])
        # data to modify
        arrayModify.append(dataFCs)
    # List of unique values
    arraySrc = list(set(arraySrc))

    # create arr of arr with adm data for each src
    arrayLine = []
    arrayTemp = []
    i = 0
    while i < len(arraySrc):
        for dataFCs in arrayModify:
            if (dataFCs.split('_')[5] == arraySrc[i]):
                arrayTemp.append(dataFCs)
        arrayLine.append(list(reversed(arrayTemp)))
        i += 1
        arrayTemp = []

    # Work with the arr of arr to delete features
    for admins in arrayLine:
        j = len(admins)
        # Only work with if there is more than one admin
        if j != 1:
            i = 0
            # Comparing higher and lower admin
            while i < j - 1:
                arcpy.AddMessage(stars)
                arcpy.AddMessage(f' Currently comparing {admins[i]} vs {admins[i + 1]}')
                arcpy.AddMessage(' ')
                # selection process where: h_admn -> admins[i + 1] and l_admn -> admins[i]
                # make a layer from the feature class
                tempLayer = arcpy.MakeFeatureLayer_management(admins[i], "l_admin")
                arcpy.SelectLayerByLocation_management(tempLayer, 'SHARE_A_LINE_SEGMENT_WITH',
                                                       admins[i + 1])
                # Check if anything has been selected
                # delete if there is a selection
                if int(arcpy.GetCount_management(tempLayer)[0]) > 0:
                    arcpy.DeleteFeatures_management(tempLayer)
                i += 1

    # Create line admin shapefiles files in 202_admn folder
    if arcpy.Exists(gdbPath):
        arcpy.env.workspace = gdbPath
        for fc in dataLine:
            folderShp = str(Path(cmf / "202_admn"))
            # arcpy.Delete_management(folderShp)
            # Intersect output to shp
            arcpy.FeatureClassToShapefile_conversion([fc], str(Path(cmf / "202_admn")))
        
    arcpy.AddMessage(stars)
    arcpy.AddMessage(' Process ended succesfully')

except Exception:
    e = sys.exc_info()[1]
    arcpy.AddError(e.args[0])
    arcpy.AddMessage(stars)
    arcpy.AddMessage(e.args[0])
    arcpy.AddMessage(' Something weird happened connected to last progress message...')
    sys.exit()
