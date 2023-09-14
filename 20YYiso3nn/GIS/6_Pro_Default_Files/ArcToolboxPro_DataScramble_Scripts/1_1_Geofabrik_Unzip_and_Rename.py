# -*- coding: utf-8 -*-
"""==============================================================================
  
Title          :1_1_Geofabrik_Unzip_and_Rename.py
Description    :Unzip geofabrik OSM data and put data into the respective locations
Author         :Tom H, Darren C and LF Velasquez
Date           :2023-09-14
Version        :1.0
Usage          :Inside ArcPro as part of the MapAction_Data_Scramble_2023.atbx
Notes          :This script must be run as part of the MapAction_Data_Scramble_2023.atbx
                in ArcPro, as otherwise it will return an error as part of the user input
python version  :3.9.16 as per ArcPro 3.1 sys.version
 
=============================================================================="""

import os, shutil, glob
from zipfile import ZipFile
import arcpy
from pathlib import Path
arcpy.env.overwriteOutput = True

# Ask for folder with zip file
zipfolder = Path(arcpy.GetParameterAsText(0))

# Ask for output folder - Active folder 
outputroot = Path(arcpy.GetParameterAsText(1))

# Ask for polygon to be used in the clipping action
clip_shp = arcpy.GetParameterAsText(2)

# Ask Country code
'''This is meant to deal with the issue of the country name for some countries
where Geofabrik packs several countries in one'''
countrycode = arcpy.GetParameterAsText(3).lower()

# Function to clip line datasets
def clip_osm(input_shp, clip_shp, out_folder):
    """This function will clip any line dataset
    to the polygon enter by the user

    Args:
        input_shp (str): path to the shapefile to be clipped
        clip_shp (str): path to the shapefile to be used as the clip
        out_folder (str): path to the respective folder
    """
    arcpy.analysis.Clip(input_shp, clip_shp, out_folder)

# Function to rename multiple files
def rename():
    """This function will rename and place the data in their
    respective location in the active folder
    """

    for filename in os.listdir(unzipfolder):
        #if filename.endswith(".zip"):
        cfilename, cfile_extension = os.path.splitext(filename) # split .shp file name and extension
        src = Path(unzipfolder / filename)
        
        if cfilename == "gis_osm_places_free_1":
            dst = Path(stlefolder / f'{settlename}{cfile_extension}')
            if cfile_extension.endswith(".shp"):
                clip_osm(str(src), str(clip_shp), str(dst))
                print("Clipping " + filename + " to " + settlename + cfile_extension)
                
        elif cfilename == "gis_osm_places_a_free_1":
            dst = Path(stlefolder / f'{settlepyname}{cfile_extension}')
            if cfile_extension.endswith(".shp"):
                clip_osm(str(src), str(clip_shp), str(dst))
                print("Clipping " + filename + " to " + settlepyname + cfile_extension)

        elif cfilename == "gis_osm_railways_free_1":
            dst = Path(tranfolder / f'{railname}{cfile_extension}')
            if cfile_extension.endswith(".shp"):
                clip_osm(str(src), str(clip_shp), str(dst))
                print("Clipping " + filename + " to " + railname + cfile_extension)
                
        elif cfilename == "gis_osm_roads_free_1":
            dst = Path(tranfolder / f'{roadname}{cfile_extension}')
            if cfile_extension.endswith(".shp"):
                clip_osm(str(src), str(clip_shp), str(dst))
                print("Clipping " + filename + " to " + roadname + cfile_extension)
                
        elif cfilename == "gis_osm_traffic_free_1":
            dst = Path(tranfolder / f'{traffptname}{cfile_extension}')
            if cfile_extension.endswith(".shp"):
                clip_osm(str(src), str(clip_shp), str(dst))
                print("Clipping " + filename + " to " + traffptname + cfile_extension)
                
        elif cfilename == "gis_osm_traffic_a_free_1":
            dst = Path(tranfolder / f'{traffpyname}{cfile_extension}')
            if cfile_extension.endswith(".shp"):
                clip_osm(str(src), str(clip_shp), str(dst))
                print("Clipping " + filename + " to " + traffpyname + cfile_extension)
                
        elif cfilename == "gis_osm_transport_free_1":
            dst = Path(tranfolder / f'{transptname}{cfile_extension}')
            if cfile_extension.endswith(".shp"):
                clip_osm(str(src), str(clip_shp), str(dst))
                print("Clipping " + filename + " to " + transptname + cfile_extension)
                
        elif cfilename == "gis_osm_transport_a_free_1":
            dst = Path(tranfolder / f'{transpyname}{cfile_extension}')
            if cfile_extension.endswith(".shp"):
                clip_osm(str(src), str(clip_shp), str(dst))
                print("Clipping " + filename + " to " + transpyname + cfile_extension)
                
        elif cfilename == "gis_osm_water_a_free_1":
            dst = Path(physfolder / f'{waterbodiesname}{cfile_extension}')
            if cfile_extension.endswith(".shp"):
                clip_osm(str(src), str(clip_shp), str(dst))
                print("Clipping " + filename + " to " + waterbodiesname + cfile_extension)

        elif cfilename == "gis_osm_waterways_free_1":
            dst = Path(physfolder / f'{waterwaysname}{cfile_extension}')
            if cfile_extension.endswith(".shp"):
                clip_osm(str(src), str(clip_shp), str(dst))
                print("Clipping " + filename + " to " + waterwaysname + cfile_extension)
                
        elif cfilename == "gis_osm_natural_free_1":
            dst = Path(physfolder / f'{naturalptname}{cfile_extension}')
            if cfile_extension.endswith(".shp"):
                clip_osm(str(src), str(clip_shp), str(dst))
                print("Clipping " + filename + " to " + naturalptname + cfile_extension)
                
        elif cfilename == "gis_osm_natural_a_free_1":
            dst = Path(physfolder / f'{naturalpyname}{cfile_extension}')
            if cfile_extension.endswith(".shp"):
                clip_osm(str(src), str(clip_shp), str(dst))
                print("Clipping " + filename + " to " + naturalpyname + cfile_extension)
                
        elif cfilename == "gis_osm_pofw_free_1":
            dst = Path(poisfolder / f'{powptname}{cfile_extension}')
            if cfile_extension.endswith(".shp"):
                clip_osm(str(src), str(clip_shp), str(dst))
                print("Clipping " + filename + " to " + powptname + cfile_extension)
                
        elif cfilename == "gis_osm_pofw_a_free_1":
            dst = Path(poisfolder / f'{powpyname}{cfile_extension}')
            if cfile_extension.endswith(".shp"):
                clip_osm(str(src), str(clip_shp), str(dst))
                print("Clipping " + filename + " to " + powpyname + cfile_extension)
                
        elif cfilename == "gis_osm_pois_free_1":
            dst = Path(poisfolder / f'{poisptname}{cfile_extension}')
            if cfile_extension.endswith(".shp"):
                clip_osm(str(src), str(clip_shp), str(dst))
                print("Clipping " + filename + " to " + poisptname + cfile_extension)
                
        elif cfilename == "gis_osm_pois_a_free_1":
            dst = Path(poisfolder / f'{poispyname}{cfile_extension}')
            if cfile_extension.endswith(".shp"):
                clip_osm(str(src), str(clip_shp), str(dst))
                print("Clipping " + filename + " to " + poispyname + cfile_extension)
                
        elif cfilename == "gis_osm_buildings_a_free_1":
            dst = Path(bldgfolder / f'{bldgname}{cfile_extension}')
            if cfile_extension.endswith(".shp"):
                clip_osm(str(src), str(clip_shp), str(dst))
                print("Clipping " + filename + " to " + bldgname + cfile_extension)
                
        elif cfilename == "gis_osm_landuse_a_free_1":
            dst = Path(landfolder / f'{landname}{cfile_extension}')
            if cfile_extension.endswith(".shp"):
                clip_osm(str(src), str(clip_shp), str(dst))
                print("Clipping " + filename + " to " + landname + cfile_extension)

zipcounter = len(glob.glob1(zipfolder,"*.zip"))
arcpy.AddMessage("Number of zips: " + str(zipcounter))

# Work with the zip file
for zipname in os.listdir(zipfolder):
    if zipname.endswith(".zip"):
        zipfile = Path(zipfolder / zipname)

        if zipcounter > 1:
            outputfolder = Path(outputroot / countrycode.upper())  # Use country folder if there is more than one zip file
        else:
            outputfolder = outputroot #+ countrycode.upper()  # Remove county folder from output Path for MapAction version - data written to 02_Active_Data

        arcpy.AddMessage(" ")
        arcpy.AddMessage(f"> Processing: {countrycode} ( {countrycode.upper()} ) to {outputfolder}")

        unzipfolder = Path(outputfolder / "_TEMP_UNZIP")

        if not os.path.exists(outputfolder): # checks output subdirectory existence
            os.makedirs(outputfolder) # creates output subdirectory if it does not exist
        if not os.path.exists(unzipfolder): # checks output subdirectory existence
            os.makedirs(unzipfolder) # creates output subdirectory if it does not exist

        # Unzip files here
        zf = ZipFile(zipfile, 'r')
        zf.extractall(unzipfolder)
        zf.close()

        # Declare folders
        stlefolder = Path(outputfolder / "229_stle")
        if not os.path.exists(stlefolder): # checks output subdirectory existence
            os.makedirs(stlefolder) # creates output subdirectory if it does not exist
        tranfolder = Path(outputfolder / "232_tran")
        if not os.path.exists(tranfolder): # checks output subdirectory existence
            os.makedirs(tranfolder) # creates output subdirectory if it does not exist
        physfolder = Path(outputfolder / "221_phys")
        if not os.path.exists(physfolder): # checks output subdirectory existence
            os.makedirs(physfolder) # creates output subdirectory if it does not exist
        poisfolder = Path(outputfolder / "222_pois")
        if not os.path.exists(poisfolder): # checks output subdirectory existence
            os.makedirs(poisfolder) # creates output subdirectory if it does not exist
        bldgfolder = Path(outputfolder / "206_bldg")
        if not os.path.exists(bldgfolder): # checks output subdirectory existence
            os.makedirs(bldgfolder) # creates output subdirectory if it does not exist
        landfolder = Path(outputfolder / "218_land")
        if not os.path.exists(landfolder): # checks output subdirectory existence
            os.makedirs(landfolder) # creates output subdirectory if it does not exist

        # Declare file names
        settlename = countrycode + "_stle_stl_pt_s0_osm_pp_settlements"
        settlepyname = countrycode + "_stle_stl_py_s0_osm_pp_settlements"
        roadname = countrycode + "_tran_rds_ln_s0_osm_pp_roads"
        railname = countrycode + "_tran_rrd_ln_s0_osm_pp_railways"
        traffptname = countrycode + "_tran_trf_pt_s0_osm_pp_traffic"
        traffpyname = countrycode + "_tran_trf_py_s0_osm_pp_traffic"
        transptname = countrycode + "_tran_trn_pt_s0_osm_pp_transport"
        transpyname = countrycode + "_tran_trn_py_s0_osm_pp_transport"
        waterwaysname = countrycode + "_phys_riv_ln_s0_osm_pp_rivers"
        waterbodiesname = countrycode + "_phys_lak_py_s0_osm_pp_waterbodies"
        naturalptname = countrycode + "_phys_nat_pt_s0_osm_pp_natural"
        naturalpyname = countrycode + "_phys_nat_py_s0_osm_pp_natural"
        powptname = countrycode + "_pois_rel_pt_s0_osm_pp_placeofworship"
        powpyname = countrycode + "_pois_rel_py_s0_osm_pp_placeofworship"
        poisptname = countrycode + "_pois_poi_pt_s0_osm_pp_pointsofinterest"
        poispyname = countrycode + "_pois_poi_py_s0_osm_pp_pointsofinterest"
        bldgname = countrycode + "_bldg_bdg_py_s0_osm_pp_buildings"
        landname = countrycode + "_land_lnd_py_s0_osm_pp_landuse"

        # Calling main() function
        rename()
        del countrycode

        # Delete unzip dictionary
        shutil.rmtree(unzipfolder, ignore_errors=False, onerror=None)