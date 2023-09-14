# -*- coding: utf-8 -*-
"""==============================================================================
  
Title          :2_2_4_Apply_Correct_Field_Names.py
Description    :Rename fields for ADMN1, ADMN 2, ADMN 3, ADMN 4
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

import os
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

# Ask for inputs inside ArcPro
# This need setting insidde the toolbox script properties
inFeatures = arcpy.GetParameterAsText(0)
ad1Mapping = arcpy.GetParameterAsText(1)
ad2Mapping = arcpy.GetParameterAsText(2)
ad3Mapping = arcpy.GetParameterAsText(3)
ad4Mapping = arcpy.GetParameterAsText(4)

# Set the field and geodatabase names
ADM1_PCODE = "ADM1_PCODE"
ADM2_PCODE = "ADM2_PCODE"
ADM3_PCODE = "ADM3_PCODE"
ADM4_PCODE = "ADM4_PCODE"
gdbName = "tempGDB.gdb"

# Defining the right path were the files need to be at the end
lyrPath = arcpy.Describe(inFeatures).path
admPath = Path(lyrPath).parent.parent
gdbfldr = "2_Active_Data/202_admn" + sep + gdbName
gdbPath = str(Path(admPath / gdbfldr))
fileName = Path(lyrPath).stem

# Delete then create working geoDatabase
if arcpy.Exists(gdbPath):
    arcpy.Delete_management(gdbPath)
arcpy.CreateFileGDB_management(str(Path(admPath / gdbfldr).parent), gdbName)

# Create the feature class in geoDatabase
arcpy.AddMessage(stars)
arcpy.AddMessage(' Admin 1 field was {} but is now {}'.format(ad1Mapping, ADM1_PCODE))
arcpy.AddMessage(' Admin 2 field was {} but is now {}'.format(ad2Mapping, ADM2_PCODE))
arcpy.AddMessage(' Admin 3 field was {} but is now {}'.format(ad3Mapping, ADM3_PCODE))
arcpy.AddMessage(' Admin 4 field was {} but is now {}'.format(ad4Mapping, ADM4_PCODE))
arcpy.AddMessage(' ')
featureGDB = str(Path(Path(gdbPath) / (arcpy.Describe(inFeatures).name).split('.')[0]))

# Copy shapefile to feature class
arcpy.CopyFeatures_management(inFeatures, featureGDB)

# Alfter field name including alias inside the geodatabase
arcpy.AlterField_management(featureGDB, ad1Mapping, ADM1_PCODE, ADM1_PCODE)
arcpy.AlterField_management(featureGDB, ad2Mapping, ADM2_PCODE, ADM2_PCODE)
arcpy.AlterField_management(featureGDB, ad3Mapping, ADM3_PCODE, ADM3_PCODE)
arcpy.AlterField_management(featureGDB, ad4Mapping, ADM4_PCODE, ADM4_PCODE)

# Delete original shapefilb
arcpy.Delete_management(inFeatures)

# Copy feature class toshapefile
arcpy.CopyFeatures_management(featureGDB, inFeatures)

# Tidy up working geoDatabase
if arcpy.Exists(gdbPath):
    arcpy.Delete_management(gdbPath)

# Make sure to add the layer back into the active map
aprx     = arcpy.mp.ArcGISProject("CURRENT")
frame_name = aprx.activeMap.name
mframe = aprx.listMaps(frame_name)[0]
mframe.addDataFromPath(inFeatures)
