# -*- coding: utf-8 -*-
"""==============================================================================
  
Title          :2_5_Split_Line_Work_HDX.py
Description    :Split line work in .gdb downloaded from HDX
Author         :LF Velasquez
Date           :2024-02-07
Version        :1.0
Usage          :Inside ArcPro as part of the MapAction_Data_Scramble_2023.atbx
Notes          :- This script must be run as part of the MapAction_Data_Scramble_2023.atbx
                in ArcPro, as otherwise it will return an error as part of the user input
                - The polygon data needs to exist in the 202_admn folder
                - This is script assumes that the data entered has the following name convention
                iso_adminDescription_dataDescrition_mgn_source_lastRevisionDate as per HDX convention
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
    # Ask for the admn polygon to be used
    inFeatures  = arcpy.GetParameterAsText(0)
    
    # Ask for the type of process needed
    inField  = arcpy.GetParameterAsText(1)
    
    # Ask for lowest adming level
    admn_lvl  = arcpy.GetParameterAsText(2)
    
    # Set path to active data folder
    actv_path = Path( Path().resolve().parents[1] / '2_Active_Data')
    
    # Get the names of the polygon files
    '''This is needed to put the right suffix to the line file'''
    arcpy.env.workspace = str(Path(actv_path / "202_admn"))
    _pyFcList = arcpy.ListFeatureClasses("*py*")
    
    # Remove the wrl layer
    for lyr_name in _pyFcList:
        if 'wrl' in lyr_name:
            _pyFcList.remove(lyr_name)
            
    arcpy.AddMessage(_pyFcList)
    
    # Select by attribute
    '''administration areas are represented by the numbers
    0, 1, 2 and so on, coastline is represented by 99'''

    # put unique field values into an order list 
    with arcpy.da.SearchCursor(inFeatures, inField) as cursor:
        lst_admnLevel = (sorted({row[0] for row in cursor}))
        
    # Build list with values to be used in selection
    # list to control loop - should be admin and coastline
    lst_slct = [x for x in lst_admnLevel if x <= int(admn_lvl) or x == 99]
    
    # list to control naming of admin files
    lst_admn = [x for x in lst_admnLevel if x <= int(admn_lvl)]
    
    # list for disputed boundaries
    lst_dspt = [x for x in lst_admnLevel if x > int(admn_lvl) and x != 99]

    
    for value in lst_slct:
        sel_records = arcpy.management.SelectLayerByAttribute(inFeatures, 
                                                              'NEW_SELECTION', 
                                                              f'"{inField}" = {value}')
        arcpy.AddMessage(f'this is admin value {value} and this is the selection {arcpy.management.GetCount(sel_records)}')
        
        # selection to shp file in the right location and right name
        # 1. for admn data
        if value in lst_admn:
        
            arcpy.AddMessage(f'Creating line shapefile for admn {value}')
            # create name for ln shapefile
            _pySHP = next((shp for shp in _pyFcList if f'admn_ad{value}' in shp), None)
            arcpy.AddMessage(_pySHP)
            _lnSHP = _pySHP.replace('_py_', '_ln_')
            
            # create shapefile
            arcpy.management.CopyFeatures(sel_records, str(Path(actv_path / f'202_admn/{_lnSHP}')))
        
        # 2. for coastline
        if value == 99:
            
            arcpy.AddMessage(f'Creating line shapefile for admn {value}')
            
            # create file name
            iso_code = Path(inFeatures).name.split('_')[0]
            data_src = Path(inFeatures).name.split('_')[-2]
            filename = f'{iso_code}_elev_cst_ln_s0_{data_src}_pp_coastline'
            
            # create shapefile
            arcpy.management.CopyFeatures(sel_records, str(Path(actv_path / f'211_elev/{filename}')))
        
    # 3. For disputed boundaries - this needs to be outside loop as all values are selected at once
    
    # make sure there are disputed boundaries
    if len(lst_dspt) != 0:
        sel_records = arcpy.management.SelectLayerByAttribute(inFeatures, 
                                                                'NEW_SELECTION', 
                                                                
                                                                f'"{inField}" IN {tuple(lst_dspt)}')
        arcpy.AddMessage(f'this is admin value {value} and this is the selection {arcpy.management.GetCount(sel_records)}')
        
        arcpy.AddMessage(f'Creating line shapefile for admn {value}')
        
        # create file name
        iso_code = Path(inFeatures).name.split('_')[0]
        data_src = Path(inFeatures).name.split('_')[-2]
        filename = f'{iso_code}_admn_ad0_ln_s0_{data_src}_pp_disputedBoundaries'
    
        # create shapefile
        arcpy.management.CopyFeatures(sel_records, str(Path(actv_path / f'202_admn/{filename}')))
 
    arcpy.AddMessage(stars)
    arcpy.AddMessage(' Process ended succesfully')

except Exception:
    e = sys.exc_info()[1]
    arcpy.AddError(e.args[0])
    arcpy.AddMessage(stars)
    arcpy.AddMessage(e.args[0])
    arcpy.AddMessage(' Something weird happened connected to last progress message...')
    sys.exit()