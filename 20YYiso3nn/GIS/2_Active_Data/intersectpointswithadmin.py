import os
import sys
# These are required for DConnaghan MapAction laptop-91 as some strange python settings
# sys.path.append("C:\\py27arcgis106\\ArcGIS10.6\\Lib\\site-packages")
# sys.path.append(r"C:\Program Files (x86)\ArcGIS\Desktop10.6\arcpy")
# sys.path.append(r"C:\Program Files (x86)\ArcGIS\Desktop10.6\ArcToolbox\Scripts")
# sys.path.append(r"C:\Program Files (x86)\ArcGIS\Desktop10.6\bin")
# sys.path.append("C:\\py27arcgis106\\ArcGIS10.6\\Lib")
import arcpy
import datetime

# =============================================================================
# Intersect point datasets with lowest Admin data
# =============================================================================
def main(sep, admn_dir, fold_names, 
         display_split, python_dir):

    # create temporay gdb to be used in the alter field process
    arcpy.env.workspace = python_dir
    gdbName = "tempGDB.gdb"
    gdbPath = python_dir + '/' + gdbName

    # if gdb exist before creation, delete it
    if arcpy.Exists(gdbPath):
        arcpy.Delete_management(gdbPath)

    arcpy.CreateFileGDB_management(python_dir, gdbName)

    # # define crs for gdb - will avoid the reporjection step
    # sr = arcpy.SpatialReference("<add WGS 1984>")
    # arcpy.DefineProjection_management(gdbPath, sr)

    # # list of shp files
    arcpy.env.workspace = admn_dir
    arcpy.env.overwriteOutput = True
    data_fc = arcpy.ListFeatureClasses(feature_type='Polygon')


    # list py options for the user
    count = 0
    print('\nHere is the list of adm files:')
    for shp in data_fc:
        print('{}: {}'.format(count + 1, data_fc[count]))
        count += 1
    # make sure user input is a single number
    check = False
    intersect_q = '\nEnter shapefile to be used in intersect e.g. 1,2,3:\n  '
    while check is False:
        try:
            admn_idx = int((raw_input(intersect_q)))
            admn_bdr = admn_dir + '/' + data_fc[admn_idx - 1]
            admn_gdb = gdbPath + '/' + "temp_" + shp.split('.')[0]
            # copy admn to gdb
            arcpy.CopyFeatures_management(admn_bdr, admn_gdb)
            # break loop if input is correct
            check = True
        except ValueError:
            print('Try again, you entered more than one option or text:')
            intersect_q = '\nEnter shapefile to be used in intersect e.g. 1,2,3:\n'

    # Intersect process
    arr_folders = ["215_heal", "229_stle", "232_tran"]
 
    # loop through the folders with point data
    for key, value in fold_names.items():
        if value in arr_folders:
            print(display_split)
            print('Working in folder {}'.format(value))
            folder_path = python_dir + '/' + value
            arcpy.env.workspace = folder_path
            arr_pointFc = arcpy.ListFeatureClasses(feature_type='Point')
            # check if folder is empty or does not have pt data
            if len(arr_pointFc) > 0:
                for ptFc in arr_pointFc:
                    intersect_out = ''
                    # copy to gdb ready for intersect
                    pt_shp = folder_path + '/' + ptFc
                    pt_gdb = gdbPath + '/' + ptFc.split('.')[0]
                    arcpy.CopyFeatures_management(pt_shp, pt_gdb)
                    # intersect work
                    intersect_out = gdbPath + '/' + ptFc.split('.')[0]
                    arcpy.Intersect_analysis([ptFc, admn_gdb], intersect_out, "", "", "POINT")
                    # delete existing shp file
                    arcpy.Delete_management(pt_shp)
                    # intersect output to shp
                    arcpy.FeatureClassToShapefile_conversion([intersect_out], folder_path)
            else:
                print('Folder {} does not have point data to be intersected with admn'.format(value))
                print(display_split)
    # Delete temp gdb
    if arcpy.Exists(gdbPath):
        arcpy.Delete_management(gdbPath)
    print(display_split)
    print('Process ended succesfully. Moving to Delete Concident Layers')
    print(display_split)