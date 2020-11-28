# -*- coding: utf-8 -*-
"""==============================================================================

 Title          :gisCircle_fieldSelection_v14.py
 Description    :Converting source field name to match required names for automation
 Author         :LF Velasquez - MA
 Amended by     :DJ Connaghan - MA
 Date           :Oct 16 2020
 Version        :0.14
 Usage          :gisCircle_fieldSelection_v14.py
 Notes          : Need to write here the order of the proces and things that need to exist
                  for the script to run as intended
 python version :2.7.12

=============================================================================="""

# =============================================================================
# Modules - Libraries
# =============================================================================
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

import setglobalvariables
import convertpolytoline
import intersectpointswithadmin
import applycorrectfieldnames
import deletecoincidentlayers

###############################################################################
##  This is the main section calling all sub-processes
###############################################################################
if __name__ == "__main__":

    arcpy.env.overwriteOutput = True
    strTime = datetime.datetime.now()

###############################################################################
##  setglobalvariables
##  set all variables to be used, it's easier & cleaner if in separate section
###############################################################################

    sep, arr_files, crs_error, adm_names, pnt_names, stl_names, python_dir, admn_dir, display_split = setglobalvariables.main()

###############################################################################
##  Apply correct field names to datasets for labelling & definition queries
###############################################################################

#    works!!
#    need to develop a loop that runs through adm_names, stl_names, air_names etc

    for key, value in sorted(pnt_names.items()):
       applycorrectfieldnames.main(sep, value, key, pnt_names, adm_names,
                                   display_split, python_dir, admn_dir)

# ###############################################################################
# ##  NO LONGER NEEDED - Take the admin polygon data and convert to linework
# ###############################################################################

# #    works!!
#     convertpolytoline.main(sep, arr_files, adm_names, admn_dir,
#                            display_split, python_dir)

# ###############################################################################
# ##  Run intersect point with admin as a loop, currently based on the dict key,
# ##  it might need changing if the key brings more than one shp file at the time
# ###############################################################################

# #    works!!
#     for key, value in sorted(pnt_names.items()):
#         intersectpointswithadmin.main(sep, arr_files, adm_names, admn_dir, value,
#                                       key, pnt_names, display_split, python_dir)

# # ###############################################################################
# # ##  Extract higher level admin boundaries from lower level admin boundaries
# # ###############################################################################

# #    works!!
    # deletecoincidentlayers.main(sep, display_split, python_dir, admn_dir)
