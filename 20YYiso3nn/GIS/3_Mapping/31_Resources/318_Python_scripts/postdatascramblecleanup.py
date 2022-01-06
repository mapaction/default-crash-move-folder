# -*- coding: utf-8 -*-
"""==============================================================================

 Title          :postdatascramblecleanup.py
 Description    :Converting source field name to match required names for automation
 Author         :LF Velasquez - MA
 Amended by     :DJ Connaghan - MA
 Date           :Nov 16 2020
 Version        :1.0
 Usage          :postdatascramblecleanup.py
 Notes          : 
                - Version 1.0 only works for folders 202, 215, 229, 232
                - The order of this process is as follow:
                    1. Correct field names
                    2. Intersect point dataset with admin boundary
                    3. Delete coincident layes for admin boundaries line work
 python version :2.7.12

=============================================================================="""

# =============================================================================
# Modules - Libraries
# =============================================================================
import os
import sys
# These are required for DConnaghan MapAction laptop-91 as some strange python settings
sys.path.append('..' + os.path.sep + '2_Active_Data')
sys.path.append("C:\\python27\\ArcGIS10.8\\Lib\\site-packages")
sys.path.append(r"C:\Program Files (x86)\ArcGIS\Desktop10.8\arcpy")
sys.path.append(r"C:\Program Files (x86)\ArcGIS\Desktop10.8\ArcToolbox\Scripts")
sys.path.append(r"C:\Program Files (x86)\ArcGIS\Desktop10.8\bin")
sys.path.append("C:\\python27\\ArcGIS10.8\\Lib")
import arcpy
import datetime
import setglobalvariables
import convertpolytoline
import intersectpointswithadmin
import applycorrectfieldnames
import deletecoincidentlayers

###############################################################################
##  This is the main section calling all sub-processes
###############################################################################
if __name__ == "__main__":

###############################################################################
##  setglobalvariables
##  set all variables to be used, it's easier & cleaner if in separate section
###############################################################################

    sep, crs_error, arr_folder, fold_names, admn_names, stle_names, airp_names, port_names, heal_names, python_dir, admn_dir, display_split = setglobalvariables.main()

###############################################################################
##  Making sure the folders needed exist
##############################################################################
    new_dir = []
    for fld in arr_folder:
        dir_path = python_dir + '/' + fld
        if fld == '202_admn':
            if os.path.isdir(dir_path) is False:
                print(display_split)
                print('You need to have at least data in folder 202_admin to be able to run this tool')
                print(display_split)
                exit()
        if os.path.isdir(dir_path) is False:
            os.mkdir(dir_path)
            new_dir.append(fld)
    print(display_split)
    # put this in a loop, if no folders generated, don't print
    print('The tool created folders: {}'.format(new_dir))
    print(display_split)
    print('Starting the work')

#############################################################################
## Apply correct field names to datasets for labelling & definition queries
#############################################################################
    print(display_split)
    print('Correcting Field Names')
    print(display_split)
    applycorrectfieldnames.main(sep, fold_names, admn_names, stle_names,
                                airp_names, port_names, heal_names,
                                display_split, python_dir, admn_dir)

###############################################################################
##  Add adm and pcode field to point datasets
###############################################################################
    print(display_split)
    print('Intersecting points with Admin boundaries')
    print(display_split)
    intersectpointswithadmin.main(sep, admn_dir, fold_names, 
                                  display_split, python_dir)

###############################################################################
##  Extract higher level admin boundaries from lower level admin boundaries
###############################################################################
    print(display_split)
    print('Deleting coincident layers')
    print(display_split)
    deletecoincidentlayers.main(sep, display_split, python_dir, admn_dir)
