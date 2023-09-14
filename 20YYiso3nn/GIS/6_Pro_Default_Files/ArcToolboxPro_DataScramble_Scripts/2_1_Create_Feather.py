# -*- coding: utf-8 -*-
"""==============================================================================
  
Title          :2_1_Create_Feather.py
Description    :Creates polygon use for feathering
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
    # Ask user to enter admin boundary to be used for a feather
    lcl_admn = Path(arcpy.GetParameterAsText(0))
    
    # Set other variables required
    # global background and country iso
    countrycode = lcl_admn.name.split("_")[0]
    glb_bckg = Path(lcl_admn.parent.parent / f"207_carto\wrl_carto_ext_py_s0_esri_pp_globalBackground.shp")
    fea_text = lcl_admn.name.split("_")[7].split(".")[0]
   
    # Erase the admin from global background
    # This will create the polygon use for the feather symbology
    # arcpy.analysis.Erase(infeature, erase_feature, out_feature)
    feather_name = f'{countrycode}_carto_fea_py_mapaction_pp_faded_{fea_text}.shp'
    feather_py = Path(lcl_admn.parent.parent / f"207_carto\{feather_name}")
    arcpy.analysis.Erase(str(glb_bckg), str(lcl_admn), str(feather_py))
    
    arcpy.AddMessage(stars)
    arcpy.AddMessage(f' Feather for {lcl_admn.name} has been created...')
    
except Exception:
    e = sys.exc_info()[1]
    arcpy.AddError(e.args[0])
    arcpy.AddMessage(stars)
    arcpy.AddMessage(e.args[0])
    arcpy.AddMessage(' Something weird happened connected to last progress message...')
    sys.exit()

