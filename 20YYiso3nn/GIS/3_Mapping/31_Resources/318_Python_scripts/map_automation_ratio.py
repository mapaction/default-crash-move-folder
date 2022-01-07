""" This scripts brings together all data and maps for the report """
import os
import arcpy
from arcpy import env
#import string

################################################################################
# Manipulating the maps so data is loaded, displayed and scaled correctly
def main(absroot, respdict, datadict):

# Response details
    for resplist in range(len(respdict)):
        respiso3 = str(respdict[resplist]['iso3'][0])
    sep = os.path.sep

# Directory location details
    datadir = absroot + sep + "2_Active_Data" + sep
    mapsdir = absroot + sep + "3_Mapping" + sep
    mxdsdir = mapsdir + "32_Map_Templates" + sep

# This calculates the ratio to define which template to use
    for datalist in range(len(datadict)):
        if datadict[datalist]['lyrs'][0] == "mainmap-admn-ad0-py-s0-scaling":
            arcpy.env.workspace = datadir + datadict[datalist]['dirs'][0]
            fcwildcard = respiso3 + "_admn_ad0_py*"
            featureclasses = arcpy.ListFeatureClasses(fcwildcard)
            for fc in featureclasses:
                zoomed = datadir + datadict[datalist]['dirs'][0] + \
                         sep + fc
                arcpy.env.workspace = zoomed
                desc = arcpy.Describe(zoomed)
                xDist = desc.extent.XMax - desc.extent.XMin
                yDist = desc.extent.YMax - desc.extent.YMin
                ratio = xDist / yDist
    if ratio >= 1.64:
        origtemp = "landscape_bottom"
    elif ratio >= 1.07 and ratio <= 1.64:
        origtemp = "landscape_side"
    else:
        origtemp = "portrait_bottom"
    origmap = mxdsdir + "arcmap-10.6_reference_" + origtemp + ".mxd"
    print origmap
    return origmap, origtemp