# -*- coding: utf-8 -*-
"""==============================================================================
  
 Title          :feathering.py
 Description    :Creating feathering for a polygon - shp or feature class
 Author         :LF Velasquez & Darren Connaghan - MapAction
 Date           :Nov 15 2021
 Version        :2.2
 Usage          :python feathering.py
 Notes          :If running python 3 the raw_input needs to be changed to input()
                    Creating the AOI before running the script.
                        1. In Layout view, double click the data frame to "focus" it.
                        2. Using the New Rectangle tool on the Draw toolbar, draw a
                            graphic that fills the extent of the page.
                        3. Switch to Data view and make the rectangle a little larger
                            than the page extent using the handles to pull box out on
                            opposite corners.
                        4. Switch back to Layout view.
                        5. Right click the data frame in the table of contents and
                            click Convert Graphics to Features.
python version  :2.7.14
 
=============================================================================="""
# =============================================================================
# Modules - Libraries
# =============================================================================
import sys
# these are the python environments for ma-laptop92
# further documentation required to set for non standard mapaction laptop
sys.path.append("C:\\py27arcgis106\\ArcGIS10.6\\Lib\\site-packages")
sys.path.append("C:\\Program Files (x86)\\ArcGIS\\Desktop10.6\\arcpy")
sys.path.append("C:\\Program Files (x86)\\ArcGIS\\Desktop10.6\\ArcToolbox\\Scripts")
sys.path.append("C:\\Program Files (x86)\\ArcGIS\\Desktop10.6\\bin")
sys.path.append("C:\\py27arcgis106\\ArcGIS10.6\\Lib")
  
# Installing pathlib package using pip - to be used when dealing with path to files
# For backwards compatibility
try:
    from pip import main as pipmain
except ImportError:
    from pip._internal import main as pipmain
pipmain(['install', 'pathlib'])

# import new package and any other packages
import os
import arcpy
import datetime
from pathlib import Path

# =============================================================================
# Functions
# =============================================================================
def _input(message, input_type=str):
    while True:
        try:
            return input_type (input(message))
        except:
            print('Please only enter a single number')
            pass
  
# =============================================================================
# Setting Global Variables
# =============================================================================
try:
    sep = os.path.sep
    startTime = datetime.datetime.now()

    # #############################################################################
    # Setting the right paths to files
    # #############################################################################

    # Get the path of the python script
    pathname = os.path.dirname(sys.argv[0])
    abs_path = Path(pathname)

    # Split the path to get rid of the 318_Script and go back to GIS folder
    main_path = abs_path.parents[2]

    # Set the path to the files in 202_admn and 207_carto
    admnpath = Path(main_path, "2_Active_Data" + sep + "202_admn")
    cartopath = Path(main_path, "2_Active_Data" + sep + "207_carto")

    # List shp files in admnpath to ask user to select the right one
    shp_fls = admnpath.glob('*0_py_s0_*.shp')
    lst_shp = [x for x in shp_fls if x.is_file()]
    print('-----')
    print('Here is the list of shp files in 202_admn')
    lst_nmb = []
    i = 1
    for shp in lst_shp:
        lst_nmb.append(i) # This will be used in the check further down the line
        print('{} - {}').format(i,shp.name)
        i += 1
    print('-----')

    # Catching error on the user input - First catch if either text or number with commas are entered
    usr_inp = _input("Select the file to be used in the feathering by entering either 1,2,3...etc: ", int)
    # Catching error on the user input - Second catch if a number that does not exist is entered
    flag = False
    while flag is False:
        if usr_inp not in lst_nmb:
            print('-----')
            print('The number you entered is not a valid option - check again in the list of files')
            usr_inp = _input("Select the file to be used in the feathering by entering either 1,2,3...etc: ", int)
        else:
            flag = True
    
    # Set the index for the admn shp file selected
    shp_idx =  usr_inp - 1
 
    # #############################################################################
    # Setting the files to be used in the main process
    # #############################################################################
    admn_shp = str(lst_shp[shp_idx])
    fth_name = lst_shp[shp_idx].name.split('_')[0] + '_carto_ext_py_s0_ma_pp.shp'
    feathaoi = str(Path(cartopath, fth_name))
    # Getting information for the rings
    distanceNumber = 10
    bufferDistance = _input('Please enter how wide in metres you would like the rings: ', int)
    distancesList = []
      
    # =============================================================================
    # Start of Main Process
    # =============================================================================
      
    # Creating distance list
    distance = bufferDistance
    for i in range(distanceNumber):
        distancesList.append(distance)
        distance += bufferDistance
    print ('--------------------------')
    print ('... creating the buffer')
    
    # Set feather output name
    featherSimple = lst_shp[shp_idx].name.split('_')[0] + '_carto_fea_py_s0_ma_simple.shp'
    featherBoundingBox = lst_shp[shp_idx].name.split('_')[0]+ '_carto_fea_py_s0_ma.shp'
    
    # Set local variables for feathering - check if exist and delete if they do - in case of re-run
    inFeatures = admn_shp
    temp = str(cartopath) + sep + 'temp.shp'
    # Check for existence of data before deleting
    if arcpy.Exists(temp):
        arcpy.Delete_management(temp)

    finalFeathering = str(cartopath) + sep + featherBoundingBox
    # Check for existence of data before deleting
    if arcpy.Exists(finalFeathering):
        arcpy.Delete_management(finalFeathering)

    outFeatureClass = str(cartopath) + sep + featherSimple
    # Check for existence of data before deleting
    if arcpy.Exists(outFeatureClass):
        arcpy.Delete_management(outFeatureClass)

    print('This is the out feature class: {}').format(outFeatureClass)
    
    bufferUnit = "meters"
    # This is the expresion I previously had and it is the one used in blogs
    invxparexpression = 'abs(10 - ((100 * !distance!)/!lg_dist!))'
    xparexpression = '100 - !InvXPar!'
    # expression = '((100 * !distance!)/!lg_dist!)' 
       
    ## Execute MultipleRingBuffer
    arcpy.MultipleRingBuffer_analysis(inFeatures, outFeatureClass,
                                      distancesList, bufferUnit, "", "ALL", "OUTSIDE_ONLY")
    print ('--------------------------')
    print ('... adding field for symbology')
    arcpy.AddField_management(outFeatureClass, "XPar", "LONG", "", "", "", "", "", "NON_REQUIRED")
    arcpy.AddField_management(outFeatureClass, "InvXPar", "LONG", "", "", "", "", "", "NON_REQUIRED")
    arcpy.AddField_management(outFeatureClass, "lg_dist", "LONG", "", "", "", "", "", "NON_REQUIRED")
    arcpy.CalculateField_management(outFeatureClass, "lg_dist", distancesList[-1], "PYTHON_9.3")
    # This has to go first due to invxparexpression
    arcpy.CalculateField_management(outFeatureClass, "InvXPar", invxparexpression, "PYTHON_9.3")
    arcpy.CalculateField_management(outFeatureClass, "XPar", xparexpression, "PYTHON_9.3")

    # Using the AOI to improve feather
    arcpy.Union_analysis([outFeatureClass, feathaoi], temp, "ALL", "","GAPS")
    arcpy.Erase_analysis(temp, admn_shp, finalFeathering)

    # Make sure that the mask layer has the right transparency
    arcpy.MakeFeatureLayer_management(finalFeathering, "feather_bndbox")
    arcpy.SelectLayerByAttribute_management("feather_bndbox", "NEW_SELECTION", "distance = 0")
    arcpy.CalculateField_management("feather_bndbox", "InvXPar", 100, "PYTHON_9.3")

    # stick these fields in an array when time allows:
    #(['lg_dist', 'field_name_ad', 'field_name_ca', 'field_name_1', 'Id'])
    try:
        arcpy.DeleteField_management(finalFeathering, ["lg_dist"])
    except:
        print ("failure to delete lg_dist")
    try:
        field_name_ad = "FID_" + lst_shp[shp_idx].name.split('_')[0] + "_ad"
        arcpy.DeleteField_management(finalFeathering, [field_name_ad])
    except:
        print ("failure to delete {}").format(field_name)
    try:
        field_name_ca = "FID_" + lst_shp[shp_idx].name.split('_')[0] + "_ca"
        arcpy.DeleteField_management(finalFeathering, [field_name_ca])
    except:
        print ("failure to delete {}").format(field_name)
    try:
        field_name_1 = "FID_" + lst_shp[shp_idx].name.split('_')[0] + "__1"
        arcpy.DeleteField_management(finalFeathering, [field_name_1])
    except:
        print ("failure to delete {}").format(field_name)
    try:
        arcpy.DeleteField_management(finalFeathering, ["Id"])
    except:
        print ("failure to delete Id")

    # Delete temp file
    arcpy.Delete_management(temp)
    arcpy.Delete_management(outFeatureClass)

    print ('--------------------------')
    print ('... creating readme file for feather display in arcmap')
    ## Set output location - add file outside of gdb if neccesary
    my_file = str(cartopath) + sep + 'feather_readme.txt'
    file = open(my_file, "w")
    file.write("The script has produced one feather options: \n"
                   "a. '<iso3n>_carto_fea_py_s0_ma.shp' - this is a feather using the AOI to create a masking option\n\n"
               "To symbolise the feather in arcmap: \n"
                   "1. On the Symbology tab, show the features using a single symbol with a white colour fill and no outline\n"
                   "2. Click the Advanced button and click Transparency\n"
                   "3. Set the field to XPar and click OK twice to see the results.")
    file.close()
  
except Exception:
    print('Have you created the AOI? - If you have not please check\n')
    print('https://mapaction.atlassian.net/wiki/spaces/giscircle/pages/6995672771/Feathering+in+ArcGIS+10.6')
    print('For other errors please get in touch with Luis or Darren for support')
    e = sys.exc_info()[1]
    print(e.args[0])
print ('--------------------------')
print ('Time running the script' + ' ' + str(datetime.datetime.now() - startTime))
print (' Check files in %s') %feathaoi
