# -*- coding: utf-8 -*-
"""==============================================================================
  
Title          :2_4_Apply_PCodes_to_Points.py
Description    :Add PCODE information to the core set of point data
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

import os, sys
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
    inFeatures  = arcpy.GetParameterAsText(0)
    
    # Set the folder with point data
    admnPos     = inFeatures.find("202_admn")
    foldArray = ["215_heal", "229_stle", "232_tran"]
    foldNames   = {'*_heal_*': '215_heal',
                '*_stle_*': '229_stle',
                '*_tran_*': '232_tran'}

    # loop through the folders with point data
    for key, value in foldNames.items():
        if value in foldArray:
            arcpy.AddMessage(stars)
            arcpy.AddMessage(' Working in folder {}'.format(value))
            arcpy.AddMessage(' ')

            # Defining the right path were the files need to be at the end
            lyrPath = arcpy.Describe(inFeatures).path
            folderPath = Path(lyrPath).parent
            
            # Get point shapefiles for each folder
            arcpy.env.workspace = str(Path(folderPath / value))
            pointFeatures = arcpy.ListFeatureClasses("*_pt_*")

            # check if the folder has point data that need pcodes
            if len(pointFeatures) > 0:
                gdbName = "tempGDB.gdb"
                gdbPath = str(Path(folderPath / f'{value}/{gdbName}'))
                
                # gdbPath = folderPath + value + sep + gdbName
                if arcpy.Exists(gdbPath):
                    arcpy.Delete_management(gdbPath)
                arcpy.CreateFileGDB_management(str(Path(folderPath / value)), gdbName)
                
                for pointFC in pointFeatures:
                    
                    # copy to gdb ready for intersect
                    pointShape = str(Path(folderPath / f'{value}/{pointFC}'))
                    intersectOut = str(Path(Path(gdbPath) / pointFC.split('.')[0]))
                    
                    # delete any previous 'ADM' fields
                    fields = arcpy.ListFields(pointShape, "ADM*")
                    for field in fields:
                        delField = field.name
                        try:
                            arcpy.DeleteField_management(pointShape, delField)
                            arcpy.AddMessage(' Deleted {}'.format(delField))
                        except:
                            arcpy.AddMessage(' Cannot delete {}'.format(delField))
                            arcpy.AddMessage(' ')
                            
                    # intersecting with lowest level admin
                    arcpy.Intersect_analysis([pointFC, inFeatures],
                                            intersectOut, "", "", "POINT")
                    
                    arcpy.AddMessage(' Intersecting {}\{}'.format(gdbName,
                                                                pointFC.split('.')[0]))
                    arcpy.AddMessage(' ')
                    # delete unnecesary fields i.e. ADM0_EN; ADM1_EN
                    fields = arcpy.ListFields(pointFC, "ADM*")
                    for field in fields:
                        delField = field.name
                        if delField[-5:] != "PCODE":
                            arcpy.DeleteField_management(intersectOut, delField)
                
                    # delete existing shp file
                    arcpy.Delete_management(pointShape)
                    # converting from feature class to shapefile
                    arcpy.AddMessage(' Converting {}'.format(intersectOut))
                    arcpy.AddMessage(' ')
                    arcpy.FeatureClassToShapefile_conversion(intersectOut, str(Path(folderPath / value)))
                    # deleting fields named 'FID'
                    fields = arcpy.ListFields(pointFC, "FID*")
                    for field in fields:
                        delField = field.name
                        try:
                            arcpy.DeleteField_management(pointFC, delField)
                            arcpy.AddMessage(' Deleted {}'.format(delField))
                        except:
                            arcpy.AddMessage(' Cannot delete {}'.format(delField))
                            arcpy.AddMessage(' ')
                    # deleting fields starting with 'Shape_'
                    fields = arcpy.ListFields(pointFC, "Shape_*")
                    for field in fields:
                        delField = field.name
                        try:
                            arcpy.DeleteField_management(pointFC, delField)
                        except:
                            arcpy.AddMessage(' Cannot delete {}'.format(delField))
                            arcpy.AddMessage(' ')
                
                # Tidy up working geoDatabase
                if arcpy.Exists(gdbPath):
                    arcpy.Delete_management(gdbPath)

            else:
                arcpy.AddMessage('   No point data in the folder {} to intersect'.format(value))
                arcpy.AddMessage(' ')
               
        else:
            arcpy.AddMessage(stars)
            arcpy.AddMessage(' Folder not present is {}'.format(value))
            arcpy.AddMessage(stars)
            arcpy.AddMessage(' ')

except Exception:
    e = sys.exc_info()[1]
    arcpy.AddError(e.args[0])
    arcpy.AddMessage(stars)
    arcpy.AddMessage(e.args[0])
    arcpy.AddMessage(' Something weird happened connected to last progress message...')
    sys.exit()