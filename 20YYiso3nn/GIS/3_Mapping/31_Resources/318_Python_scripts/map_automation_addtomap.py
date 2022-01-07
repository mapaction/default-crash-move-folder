""" This scripts changes data sources in the maps """
# ------------------------------------------------------------------------------
# esri_addtomap.py
# ------------------------------------------------------------------------------
import os
import sys
import arcpy
import string

def load(symbdir, frame, lyrstoswap, df):

    # Find the feature and replace the data source
    try:
        addData = arcpy.mapping.Layer(symbdir + os.path.sep + lyrstoswap + ".lyr")
    except:
        print "Failed to load " + symbdir + lyrstoswap
    arcpy.mapping.AddLayer(df, addData, "BOTTOM")

def swap(wildcard, fram, datafolder, df, mxd, datatoswap):

    if datatoswap[-4:] == ".shp":
        datatype = "SHAPEFILE_WORKSPACE"
    elif datatoswap[-4:] == ".tif":
        datatype = "RASTER_WORKSPACE"
    for lyr in arcpy.mapping.ListLayers(mxd, wildcard, df):
        if lyr.supports("DATASOURCE"):
            if datatype == "SHAPEFILE_WORKSPACE":
                try:
                    lyr.replaceDataSource(datafolder, datatype,
                                          datatoswap[:-4])
                except:
                    print "*  failed to replaceDataSource with shapefile",
                    print datatoswap
            elif datatype == "RASTER_WORKSPACE":
                # replace the data source
                try:
                    lyr.replaceDataSource(datafolder, datatype,
                                          datatoswap[:-4])
                except:
                    print "*  failed to replaceDataSource with raster feature class"
                    print datatoswap
