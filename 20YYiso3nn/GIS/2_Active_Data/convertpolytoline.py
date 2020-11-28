import os
import sys

# These are required for DConnaghan MapAction laptop-91 as some strange python settings
sys.path.append("C:\\py27arcgis106\\ArcGIS10.6\\Lib\\site-packages")
sys.path.append(r"C:\Program Files (x86)\ArcGIS\Desktop10.6\arcpy")
sys.path.append(r"C:\Program Files (x86)\ArcGIS\Desktop10.6\ArcToolbox\Scripts")
sys.path.append(r"C:\Program Files (x86)\ArcGIS\Desktop10.6\bin")
sys.path.append("C:\\py27arcgis106\\ArcGIS10.6\\Lib")
import arcpy
import datetime

# =============================================================================
# Convert Admin Polygons to Line work
# =============================================================================
def main(sep, arr_files, adm_names, admn_dir,
         display_split, python_dir):

    # create temporay gdb to be used in the alter field process
    gdbName = "tempGDB.gdb"
    gdbPath = os.path.join(admn_dir, gdbName)

    # if gdb exist before creation, delete it
    if arcpy.Exists(gdbPath):
        arcpy.Delete_management(gdbPath)

    arcpy.CreateFileGDB_management(admn_dir, gdbName)

    # move shp to gdb
    for fc in arr_files:
        arcpy.FeatureClassToGeodatabase_conversion(fc, gdbPath)
        # check the geometry of the fc's in the gdb
        arcpy.RepairGeometry_management(fc)
        # find the location of tis string as used to rebuild the ln fc
        lastslash = fc.rfind("_admn_")
        outfc = fc[:lastslash + 10] + "ln" + fc[lastslash + 12:]
        if arcpy.Exists(outfc):
            arcpy.Delete_management(outfc)
        arcpy.PolygonToLine_management(fc, outfc, "IDENTIFY_NEIGHBORS")

    # list of fields that can be safely deleted in order to clean the data slightly
    del_fields = ['FID', 'data', 'Shape', 'OBJECTID', 'Shape_Leng', 'Shape_Le_1', 'Shape_Area']
    # loop through fc
    for fc in arr_files:
        print (display_split)
        print("Working on fc: '{}'".format(os.path.split(fc)[-1]))
        # get list of fields for each fc
        # This is use to build the key in the dict
        i = 1
        shp_names = {}
        arr_fields = arcpy.ListFields(fc)
        # iterate through the fields
        for field in arr_fields:
            if field.name not in del_fields:
                col_name = field.name
                shp_names[i] = col_name.encode("utf-8")
                i += 1
        print (display_split)

        print("Here is the list of the fields in '{}': ".format(os.path.split(fc)[-1]))
        for key, value in sorted(shp_names.items()):
            print(key, value)

        # checking if changes need to be made
        flag = raw_input("Do you need to change any field names (y/n)?: ").lower()

        # create loop to catch any error in the user input of codes
        loop_check = False
        while loop_check is False:
            if flag == 'y':
                print (display_split)
                srce_q = "\nEnter comma separated source fields to change e.g. 1,2,4:\n  "
                srce_field = raw_input(srce_q).lower()
                print (display_split)
                print("Here is the list of the destination fields: ")
                for key, value in sorted(shp_names.items()):
                    print(key, value)
                dest_q = "Enter comma separated destination fields to match e.g. ma_1n,ma_2p,ma_4n:\n  "
                dest_field = raw_input(dest_q).lower()
                arr_srceField = srce_field.split(",")
                arr_destField = dest_field.split(",")

                # remove white space in case a comma was used at the end
                arr_srceField = [x for x in arr_srceField if x.strip()]
                # change str to int to match the shp_names dict
                arr_srceField = map(int, arr_srceField)

            else:
                # change the check to break the loop and move to next fc
                loop_check = True

    # Overwrite the existing shp with the fc in gdb and delete gdb
    if arcpy.Exists(gdbPath):
        arcpy.env.workspace = gdbPath

        # list fc in gdb
        datasets = arcpy.ListDatasets(feature_type='feature')
        datasets = [''] + datasets if datasets is not None else []

        for ds in datasets:
            # if gdb is not empty then replace shp files
            check = arcpy.ListFeatureClasses(feature_dataset=ds)
            if len(check) != 0:
                for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
                    arcpy.CopyFeatures_management(
                        fc, os.path.join(admn_dir + os.sep, fc))

        # delete gdb
        arcpy.Delete_management(gdbPath)
