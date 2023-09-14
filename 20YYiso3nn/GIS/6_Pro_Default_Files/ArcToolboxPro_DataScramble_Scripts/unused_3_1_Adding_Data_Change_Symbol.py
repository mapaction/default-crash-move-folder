# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# 2_2_Create_Mask_and_Feather.py
# Created as pure Python by Luis V on: 2019-06-19
# Updated for toolbox use by Tom H for RDSP on: 2021-03-06
# Updated by Darren C on: 2022-01-27
# Python version: 2.7.14
# ESRI version: ArcGIS Desktop 10.6.1
# ---------------------------------------------------------------------------

# =============================================================================
# Modules - Libraries
# =============================================================================

import os
import arcpy

aprx = arcpy.mp.ArcGISProject("CURRENT")
mframe = aprx.listLayouts("pro-2.8_reference_landscape_side")[0]
arcpy.env.overwriteOutput = True
sep = os.path.sep

# Set the outputMFlag and outputZFlag environments to Disabled
arcpy.env.outputMFlag = "Disabled"
arcpy.env.outputZFlag = "Disabled"

# =============================================================================
# Setting Global Variables
# =============================================================================
regAdmn   = arcpy.GetParameterAsText(0)
arcpy.AddMessage(' regAdmn    {}'.format(regAdmn))
layerxDir = os.path.join(regAdmn, '3_Mapping', '31_Resources', '312_Layer_files', '3122_arcmap')

lryxFile = 'test.lyr'
regDisplay = layerxDir + sep + lryxFile
arcpy.AddMessage(' regDisplay {}'.format(regDisplay))
dataAdmn = os.path.join(regAdmn, '2_Active_Data', '202_admn', 'reg_admn_ad0_py_s0_gadm_pp_surroundingcountries.shp')
arcpy.AddMessage(' dataAdmn   {}'.format(dataAdmn))

aprx     = arcpy.mp.ArcGISProject("CURRENT")
mFrame   = aprx.listMaps("Main map")[0]
mFrame.addDataFromPath(dataAdmn)
arcpy.env.workspace = os.path.join(regAdmn, '2_Active_Data', '202_admn')
arcpy.management.ApplySymbologyFromLayer(dataAdmn,
                                         regDisplay,
                                         None, "DEFAULT")
