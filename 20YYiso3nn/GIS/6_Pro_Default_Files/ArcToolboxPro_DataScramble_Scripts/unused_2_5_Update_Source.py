# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# 2_5_Update_Source.py
# Created as pure Python by Luis V on: 2019-06-19
# Updated for toolbox use by Tom H for RDSP on: 2021-03-06
# Updated by Darren C on: 2022-01-27
# Python version: 2.7.14
# ESRI version: ArcGIS Desktop 10.6.1
# ---------------------------------------------------------------------------


# =============================================================================
# Modules - Libraries
# =============================================================================

import os, sys
import arcpy
from pathlib import Path,PureWindowsPath

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
    # This need setting insidde the toolbox script properties
    # lcl_admn = Path(arcpy.GetParameterAsText(0))
    countrycode = 'yem'
    
    # get the connection using the map project path
    '''This will help the script work independently of the
    project location'''
    fldr_conn = aprx.folderConnections[0]['connectionString']
    
    for m in aprx.listMaps():
        arcpy.AddMessage(f"Map: {m.name}")
        
        for lyr in m.listLayers():
            # Ignore if layer is a group
            if not lyr.isGroupLayer:
                arcpy.AddMessage(f'Doing {lyr.name}...')
                # avoid hillshade layer as the connection properties are different
                if lyr.name != 'Hillshade_Elevation 250m (GMTED)':
                    arcpy.AddMessage(f'working on {lyr.connectionProperties["dataset"]}')
                    
                    # Get current source information                
                    shp_src = Path(lyr.connectionProperties['connection_info']['database'])
                    
                    # Set the end folder path i.e. 202_admn
                    fld_src = shp_src.parts[-1]
                    
                    # Get the current shapefile name and replace using the countrycode
                    shp_nam = lyr.connectionProperties['dataset'].split('_')
                    
                    # for 202_admn we need to list the shapefiles
                    '''this is required because the shapefiles are 
                    likely to have a different suffix between countries'''
                    if fld_src == '202_admn':
                        p = Path(Path(fldr_conn) / f'2_Active_Data/{fld_src}')
                        lst_shp = [i.name for i in list(p.glob("*.shp"))]
                        
                        # create two list
                        '''this will manage how file names are use in the
                        connection update'''
                        lst_main = ["_".join(i.split('_')[1:4]) for i in lst_shp]
                        
                        # Avoid any layer with the prefix wrl
                        if shp_nam[0] != 'wrl':
                            flag = "_".join(shp_nam[1:4])
                            if flag in lst_main:                             
                                # get shapefile name from list in the 202_admin folder
                                admin_shp = lst_shp[lst_main.index(flag)]
                                # arcpy.AddMessage(admin_shp)
                                # arcpy.AddMessage(flag)
                                new_name = admin_shp
                        else:
                            new_name = "_".join(shp_nam)
                        
                    else:
                        # Avoid any layer with the prefix wrl
                        if shp_nam[0] != 'wrl':
                            new_name = f'{countrycode}_{"_".join(shp_nam[1:])}'
                        else:
                            new_name = "_".join(shp_nam)
                    
                    # Get connection properties of the layer and update
                    conn_prop = lyr.connectionProperties
                    conn_prop['connection_info'] = f'{fldr_conn}\\2_Active_Data\\{fld_src}'
                    conn_prop['dataset'] = new_name
                    arcpy.AddMessage(conn_prop)
                    
                    # Update layer connection
                    lyr.updateConnectionProperties(lyr.connectionProperties, conn_prop)
                    arcpy.AddMessage(f'{lyr} Source updated')
                    arcpy.AddMessage(conn_prop)

except Exception:
    e = sys.exc_info()[1]
    arcpy.AddError(e.args[0])
    arcpy.AddMessage(stars)
    arcpy.AddMessage(e.args[0])
    arcpy.AddMessage(' Something weird happened connected to last progress message...')
    sys.exit()

