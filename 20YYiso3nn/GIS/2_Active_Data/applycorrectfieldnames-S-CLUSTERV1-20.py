import os
import sys
# These are required for DConnaghan MapAction laptop-91 as some strange python settings
# sys.path.append('..' + os.path.sep + '2_Active_Data')
# sys.path.append("C:\\py27arcgis106\\ArcGIS10.6\\Lib\\site-packages")
# sys.path.append(r"C:\Program Files (x86)\ArcGIS\Desktop10.6\arcpy")
# sys.path.append(r"C:\Program Files (x86)\ArcGIS\Desktop10.6\ArcToolbox\Scripts")
# sys.path.append(r"C:\Program Files (x86)\ArcGIS\Desktop10.6\bin")
# sys.path.append("C:\\py27arcgis106\\ArcGIS10.6\\Lib")
import arcpy
import datetime

###############################################################################
##  Correct field names so they match the layerProperties json and /lyr files
###############################################################################
def main(sep, fixF_names, admn_names, stle_names,
         airp_names, port_names, heal_names, stle_names,
         display_split, python_dir, admn_dir):

    for wildcard, folder in sorted(fixF_names.items()):
        # create temporay gdb to be used in the alter field process
        gdbName = "tempGDB.gdb"
        # gdbPath = os.path.join(python_dir + '/' + folder, gdbName)
        gdbPath = python_dir + '/' + folder + '/' + gdbName

        # if gdb exist before creation, delete it
        if arcpy.Exists(gdbPath):
            arcpy.Delete_management(gdbPath)

        arcpy.CreateFileGDB_management(python_dir + '/' + folder, gdbName)

        # set the data directory as the workspace
        arcpy.env.workspace = python_dir + '/' + folder
        # Get list of shp inside folder"
        print ("Working with data in folder: {}".format(folder))
        data_fc = arcpy.ListFeatureClasses()
        # data_fc = arcpy.ListFeatureClasses(feature_type='Polygon')
        if wildcard == "*_admn_*":
            corr_fd = admn_names
        print('this is the wildcard: {}'.format(wildcard))
        print('this is the data: {}'.format(data_fc))

sep, fixF_names, adm_names, stle_names,
                                airp_names, port_names, heal_names, stle_names, 
                                display_split, python_dir, admn_dir

                                {"*_admn_*": "202_admn",
                    "*_heal_*": "215_heal",
                    "*_stle_*": "229_stle",
                    "*_airp_*": "232_tran",
                    "*_port_*": "232_tran"}
        # # iterate through shapefiles which fit the wildcard
        # count = 0
        # shp_names = {}
        # for data_fcs in data_fc:
        #     # create copy of shp inside temp gdb 
        #     inp_shp = python_dir + '/' + folder + '/' + data_fcs
        #     out_ftc = gdbPath + '/' + "temp_" + data_fcs.split('.')[0]
        #     arcpy.CopyFeatures_management(inp_shp, out_ftc)

        #     stl_fields = arcpy.ListFields(data_fcs)
        #     for field in stl_fields:
        #         if field.editable is True:
        #             col_name = field.name
        #             shp_names[str(count)] = col_name.encode("utf-8")
        #             count += 1
        #     print("Here is the list of the fields in '{}': ".format(os.path.split(data_fcs)[-1]))
        #     order_dic = {int(k):str(v) for k,v in shp_names.items()} # This will help to print the fields in an orderly manner
        #     for key_datasets, value in sorted(order_dic.items()):
        #         print ("  " + str(key_datasets) + ", " + str(value))
        #     # checking if changes need to be made
        #     flag = raw_input("Do you need to change any field names (y/n)?: ").lower()
        #     flag_check = False
        #     while flag_check is False:
        #         if flag in ['y', 'n']:
        #             loop_check = False
        #             flag_check = True
        #         else:
        #             flag = raw_input("Do you need to change any field names (y/n)?: ").lower()

        #     # create loop for y/n answer
        #     loop_check = False
        #     while loop_check is False:
        #         if flag == 'y':
        #             srce_q = "\nEnter comma separated source fields to change e.g. 1,2,4:\n  "
        #             srce_field = raw_input(srce_q)
        #             srce_check = False
        #             while srce_check is False:
        #                 if all(elem in list(shp_names.keys()) for elem in srce_field.split(",")):
        #                 # if any([True for k,v in shp_names.items() if k in srce_field.split(",")]):
        #                     srce_check = True
        #                 else:
        #                     print("You need to select a number for the list of fields, try again!")
        #                     srce_q = "Enter comma separated source fields to change e.g. 1,2,4:\n  "
        #                     srce_field = raw_input(srce_q)
        #             print (display_split)
        #             print("Here is the list of the destination fields: ")
        #             new_count = 0
        #             for key_datasets, value in sorted(adm_names.items()):
        #                 print ("  " + str(key_datasets) + ", " + str(value))
        #                 new_count += 1
        #             # check the input is a number in the fields of the src
        #             dest_q = "Enter comma separated destination fields to match e.g. 0n, 1p, 2n:\n  "
        #             dest_field = raw_input(dest_q).lower()
        #             dest_check = False
        #             while dest_check is False:
        #                 if all(elem in list(adm_names.keys()) for elem in dest_field.split(",")):
        #                     dest_check = True
        #                 else:
        #                     print("You need to select values from the destination fields, try again!")
        #                     dest_q = "Enter comma separated destination fields to match e.g. 0n, 1p, 2n:\n  "
        #                     dest_field = raw_input(dest_q).lower()

        #             arr_srceField = srce_field.split(",")
        #             arr_destField = dest_field.split(",")

        #             # remove white space in case a comma was used at the end
        #             arr_srceField = [x for x in arr_srceField if x.strip()]
        #             # # change str to int to match the shp_names dict
        #             # arr_srceField = map(int, arr_srceField)

        #             # process to alter the field name
        #             # check the user input matches the number of fields to change
        #             # need to match the number of destination fields
        #             if (len(arr_srceField) == len(arr_destField)):
        #                 print (display_split)
        #                 print("Currently modifing: '{}'".format(os.path.split(data_fcs)[-1]))

        #                 for field_code in arr_srceField:
        #                     srceField = shp_names[field_code]
        #                     # get index to be used in ma dictionary
        #                     # this will return the idx inside a list.
        #                     # it can be use as a check if len(list) > 1

        #                     fieldIndex = [i for i, j in enumerate(
        #                         arr_srceField) if j == field_code]
        #                     destField  = adm_names[arr_destField[fieldIndex[0]]]

        #                     # changing the field name
        #                     print("Changing source field '{}' for '{}'".format(
        #                         srceField, destField))

        #                     # the alteration needs to be in the fc inside gdb
        #                     # fc_gdb = os.path.join(gdbPath, os.path.split(data_fcs)[-1].split('.')[0])
        #                     # print('check here: {}'.format(fc_gdb))
        #                     arcpy.AlterField_management(out_ftc, srceField, destField)

        #                 print (display_split)
        #                 # change the check to break the loop and move to next fc
        #                 loop_check = True
        #             else:
        #                 print (display_split)
        #                 print("You've entered a source or destination fields error "),
        #                 print(" - Make sure you enter the right codes")
        #         else:
        #             # change the check to break the loop and move to next fc
        #             loop_check = True
        #             # set dict of field name to empty for next shp       
        #     count = 0
        #     shp_names = {}
        #     print (display_split)
    
        # # Overwrite the existing shp with the fc in gdb and delete gdb
        # if arcpy.Exists(gdbPath):
        #     arcpy.env.workspace = gdbPath

        #     # list fc in gdb
        #     datasets = arcpy.ListDatasets(feature_type='feature')
        #     datasets = [''] + datasets if datasets is not None else []

        #     for ds in datasets:
        #         # if gdb is not empty then replace shp files
        #         check = arcpy.ListFeatureClasses(feature_dataset=ds)
        #         if len(check) != 0:
        #             for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
        #                 # delete existing shp file
        #                 folder_path = python_dir + '/' + folder
        #                 folder_shp = folder_path + '/' + '_'.join(fc.split('_')[1:]) + '.shp'
        #                 arcpy.Delete_management(folder_shp)
        #                 # intersect output to shp
        #                 arcpy.FeatureClassToShapefile_conversion([fc], folder_path)

        #                 # out_shp = python_dir + '/' + folder + '/' + '_'.join(fc.split('_')[1:]) + '.shp'
        #                 # arcpy.CopyFeatures_management(fc, out_shp)
        #     # delete gdb
        #     arcpy.Delete_management(gdbPath)

    print(display_split)
    print('Process ended succesfully. Moving to Intersect Points with Admin')
    print(display_split)
