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

###############################################################################
##  Code to check if Projection is GCS_WGS_1984, if no projection, project,
##  if their is a projection, reproject 
###############################################################################
def main(polygon_shp):

    print "reporohecttogscwgs1984"
#    # checking current CRS
#    for py in arr_files:
#        print py
#        spatial_ref = arcpy.Describe(py).spatialReference

#        # catch if CRS in unknown - avoid elif, it is quicker to have if statements individually
#        if spatial_ref.Name == "Unknown":
#            crs_error.append(os.path.join(admn_dir, file).encode("utf-8"))
        
#        # transform if not WGS1984
#        if spatial_ref.Name != "GCS_WGS_1984":
#            print("i am here")
#            #reprojectToGCSWGS1984(py)
#    tmp_shp = os.path.join(os.path.dirname(__file__), 'temp_shp.shp')
#    # create copy of py to overwrite source py with the rigth crs
#    arcpy.CopyFeatures_management(polygon_shp, tmp_shp)

#    # setting destination crs 
#    # there are 3 ways of setting the crs:
#    path = "C:\Users\<user>\AppData\Roaming\ESRI\Desktop10.2\ArcMap\Coordinate Systems"
#    name = "GCS_WGS_1984"
#    string = "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],\
#                PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];\
#                -400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119522E-09;\
#                0.001;0.001;IsHighPrecision"
#    dest_crs = "Choose an option from the three above"
#    out_crs = arcpy.SpatialReference(dest_crs)

#    # run the tool (input, output, target crs)
#    arcpy.Project_management(tmp_shp, polygon_shp, out_crs)

    # delete tmp shp
#    arcpy.Delete_management(tmp_shp)
#    print(arcpy.GetMessages())

###############################################################################
##  Closing arguments your honour
###############################################################################
#    if len(crs_error) != 0:
#        print display_split
#        print('Process finished without error, ccheck the following:')
#        print('  202_admn, 215_heal, 229_stle & 232_tran folders')
#        print('Time running the script' + ' ' + str(datetime.datetime.now() - strTime))
#    else:
#        print display_split
#        print('The following shapefiles have an unknown Coordinate System: {}'.format(crs_error))
#        print('The process finished without error for all other datasets, check the following:)
#        print('  202_admn, 215_heal, 229_stle & 232_tran folders')
#        print('Time running the script' + ' ' + str(datetime.datetime.now() - strTime))
