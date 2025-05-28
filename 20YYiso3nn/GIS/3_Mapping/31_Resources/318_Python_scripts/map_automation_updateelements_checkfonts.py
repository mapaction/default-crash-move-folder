""" This scripts brings together all data and maps for the report """
import os
import arcpy

################################################################################
### Manipulating the maps so data is loaded, displayed and scaled correctly
##def main(origtemp, elemdict, mxdList, mxdsout, mapnumb,
##         versnum, resppais, respglid, respprod):

# Setting up variables
sep = os.path.sep

# This does the element changing of text, location and legend image

appdir = os.getcwd()
maproot = appdir.split('31')[0]
newroot = os.path.join(maproot, "32_Map_Templates", "321_arcpro")
arcpy.env.workspace = newroot
template_to_check = newroot + sep + "pro_3.0_all_templates_DC_20250122.aprx"

p = arcpy.mp.ArcGISProject(template_to_check)
for lyt in p.listLayouts("ref_landsc_bottom*"):
    print(lyt.name)
    for txt in lyt.listElements('TEXT_ELEMENT'):
        print("  " + txt.name + ": " + str(txt.elementPositionX) + ", " + str(txt.elementPositionY))
    print('')
