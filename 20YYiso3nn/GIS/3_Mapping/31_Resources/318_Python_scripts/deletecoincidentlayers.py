# -*- coding: utf-8 -*-
import os
import sys
# sys.path.append('..' + os.path.sep + '2_Active_Data')
# sys.path.append("C:\\python27\\ArcGIS10.8\\Lib\\site-packages")
# sys.path.append(r"C:\Program Files (x86)\ArcGIS\Desktop10.8\arcpy")
# sys.path.append(r"C:\Program Files (x86)\ArcGIS\Desktop10.8\ArcToolbox\Scripts")
# sys.path.append(r"C:\Program Files (x86)\ArcGIS\Desktop10.8\bin")
# sys.path.append("C:\\python27\\ArcGIS10.8\\Lib")
import arcpy
import datetime

###############################################################################
##  Correct field names so they match the layerProperties json and /lyr files
###############################################################################
def main(sep, display_split, python_dir, admn_dir):

    # create temporay gdb to be used in the alter field process
    gdbName = "tempGDB.gdb"
    gdbPath = admn_dir + '/' + gdbName

    # if gdb exist before creation, delete it
    if arcpy.Exists(gdbPath):
        arcpy.Delete_management(gdbPath)

    arcpy.CreateFileGDB_management(admn_dir, gdbName)

    # # define crs for gdb - will avoid the reporjection step
    # sr = arcpy.SpatialReference("<add WGS 1984>")
    # arcpy.DefineProjection_management(gdbPath, sr)

    # # list of shp files
    arcpy.env.workspace = admn_dir
    arcpy.env.overwriteOutput = True
    data_fc = arcpy.ListFeatureClasses(feature_type='Polygon')

    # move shp to gdb and change to line
    print('deleting line work which is coincident with higher level admin')
    for shp in data_fc:
        # create copy of shp inside temp gdb 
        inp_shp = admn_dir + '/' + shp
        inp_ftc = gdbPath + '/' + shp.split('.')[0]
        arcpy.CopyFeatures_management(inp_shp, inp_ftc)

        # check the geometry of the fc's in the gdb
        arcpy.RepairGeometry_management(inp_ftc)
        # create line fc
        outfc_nm = shp.split('.')[0]
        outfc_ln = gdbPath + '/'+ outfc_nm.replace('py', 'ln')
        if arcpy.Exists(outfc_ln):
            arcpy.Delete_management(outfc_ln)
        arcpy.PolygonToLine_management(inp_ftc, outfc_ln, "IDENTIFY_NEIGHBORS")
    

    # create list of unique sc names for ln data only
    print(display_split)
    print('Creating list of datasets by provider...')
    print(display_split)
    arcpy.env.workspace = gdbPath
    data_ln = arcpy.ListFeatureClasses(feature_type='Line')
    arr_src = []
    arr_modify = []
    for data_fcs in data_ln:
         # src names
        arr_src.append(data_fcs.split('_')[5].encode('utf-8'))
        # data to modify
        arr_modify.append(data_fcs.encode('utf-8'))
    
    # list of unique values
    arr_src = list(set(arr_src))

    # create arr of arr with adm data for each src
    arr_ln = [] # array of array
    arr_temp = []
    i = 0
    while i < len(arr_src):
        for data_fcs in arr_modify:
            if (data_fcs.split('_')[5].encode('utf-8') == arr_src[i]):
                arr_temp.append(data_fcs.encode('utf-8'))
        arr_ln.append(list(reversed(arr_temp)))
        i += 1
        arr_temp = []

    # work with the arr of arr to delete features
    for admins in arr_ln:
        j = len(admins)
        # only work with if there are more than one adm
        if j != 1:
            i = 0
            # comparing higher and lower admin
            while i < j - 1:
                print(display_split)
                print('Currently doing {} vs {}'.format(admins[i], admins[i + 1]))
                print(display_split)
                # selection process where: h_admn -> admins[i + 1] and l_admn -> admins[i]
                # make a layer from the feature class
                temp_ly = arcpy.MakeFeatureLayer_management(admins[i], "l_admin")
                arcpy.SelectLayerByLocation_management(temp_ly, 'SHARE_A_LINE_SEGMENT_WITH', admins[i + 1])
                # Check if anything has been selected
                # delete if there is a selection
                if int(arcpy.GetCount_management(temp_ly)[0]) > 0:
                    arcpy.DeleteFeatures_management(temp_ly)
                i += 1

    # Create ln admin shp files and delete gdb
    if arcpy.Exists(gdbPath):
        arcpy.env.workspace = gdbPath
        for fc in data_ln:
            folder_shp = admn_dir + '/' + fc + '.shp'
            arcpy.Delete_management(folder_shp)
            # intersect output to shp
            arcpy.FeatureClassToShapefile_conversion([fc], admn_dir)
    print('Process ended succesfully')
    print(display_split)
    print(display_split)