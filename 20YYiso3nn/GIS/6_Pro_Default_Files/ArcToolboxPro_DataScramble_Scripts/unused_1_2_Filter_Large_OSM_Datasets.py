# ---------------------------------------------------------------------------
# Filter_Large_OSM_Datasets.py
# Created on: 2021-04-01 by Tom H
# 
# Description: Filters large OSM (Geofabrik) datasets
# ---------------------------------------------------------------------------

# Import modules
import arcpy
import os
from arcpy import env

# Environment
mxd = arcpy.mapping.MapDocument("CURRENT")
df = mxd.activeDataFrame
arcpy.env.overwriteOutput=True

# Local variables:
inputshp = arcpy.GetParameterAsText(0)
filepath, ext = os.path.splitext(inputshp)
path, filename = os.path.split(filepath)
arcpy.AddMessage(" ")
arcpy.AddMessage("   > Input = " + filename + ext)
outputshp = path + os.sep + filename + "_filtered.shp"
#arcpy.AddMessage(" ")
#arcpy.AddMessage("   > Output = " + filename + "_filtered.shp")

# Define expressions (for messages only - the actual expressions used are in the SelectLayerByAttribute_management functions below.
# Saves farting about with SQL formatting)
rdsexp = "\"fclass\" = 'motorway' OR \"fclass\" = 'motorway_link' OR \"fclass\" = 'primary' OR \"fclass\" = 'primary_link'"
stlexp = "\"fclass\" = 'city' OR \"fclass\" = 'town' OR \"fclass\" = 'national_capital'"
rivexp = "\"fclass\" = 'river' OR \"fclass\" = 'canal'"

# Get input theme from DNC - from James' data poll script
parts = filename.split('_')
sectionDict = {
        0: r'geoextent',
        1: r'catetory',
        2: r'theme',
        3: r'geometry',
        4: r'scale',
        5: r'source',
        6: r'permission',
        7: r'DNCmetadata'
        }
if len(parts) < 6:
    arcpy.AddMessage(" ") 
    arcpy.AddMessage("   X - Input name does not meet DNC standard. Quitting... ")
    arcpy.AddMessage(" ")
    sys.exit()
    
# Get each part of the name    
geoextent = parts[0]
category = parts[1]
theme = parts[2]
geometry = parts[3]
scale = parts[4]
source = parts[5]

# Check that the theme is allowed
while theme not in ['rds', 'stl', 'riv']:
    arcpy.AddMessage(" ") 
    arcpy.AddMessage("   X - Dataset is not a road, river or settlement layer. Quitting...")
    arcpy.AddMessage(" ")
    sys.exit()

arcpy.AddMessage(" ") 
arcpy.AddMessage("   > Data theme = " + theme)

#Check the fclass field exists
#arcpy.AddMessage("> Performing checks...")
to_check = ['fclass'] #Create a list of field names that are required
fieldList = arcpy.ListFields(inputshp)        #Create a list of existing field names
fieldName = [f.name for f in fieldList]

for field in to_check:
  if field in fieldName:
    #arcpy.AddMessage("   - " + field + " field OK...")
    continue
  else:
    arcpy.AddMessage(" ")
    arcpy.AddMessage("   X - Field called '" + field + "' doesn't exist. Check source data and correct.")
    arcpy.AddMessage(" ")
    sys.exit(0)


# Make Layer for selection
arcpy.MakeFeatureLayer_management (inputshp, "inputlyr")
arcpy.SelectLayerByAttribute_management("inputlyr", "CLEAR_SELECTION")  

# Perform selection based on theme
if theme == 'rds':
    exptouse = rdsexp
    arcpy.SelectLayerByAttribute_management("inputlyr", "NEW_SELECTION", "\"fclass\" = 'motorway' OR \"fclass\" = 'motorway_link' OR \"fclass\" = 'primary' OR \"fclass\" = 'primary_link'")
elif theme == 'stl':
    exptouse = stlexp
    arcpy.SelectLayerByAttribute_management("inputlyr", "NEW_SELECTION", "\"fclass\" = 'city' OR \"fclass\" = 'town' OR \"fclass\" = 'national_capital'")
elif theme == 'riv':
    exptouse = rivexp
    arcpy.SelectLayerByAttribute_management("inputlyr", "NEW_SELECTION", "\"fclass\" = 'river' OR \"fclass\" = 'canal'")
else:
    arcpy.AddMessage("Dataset does not have a theme that is associated with a filtering expression. Quitting")
    sys.exit()
  
arcpy.AddMessage(" ")    
arcpy.AddMessage("   > Filtering: " + exptouse)


# Process: Copy Features
arcpy.CopyFeatures_management("inputlyr", outputshp)

arcpy.AddMessage(" ")  
arcpy.AddMessage("   > Saving filtered dataset...") 

# Process: Select Layer By Attribute
arcpy.SelectLayerByAttribute_management("inputlyr", "CLEAR_SELECTION")

# Add new layer to map
addLayer = arcpy.mapping.Layer(outputshp)
arcpy.mapping.AddLayer(df, addLayer, "TOP")
arcpy.RefreshActiveView()

# Finish Script
arcpy.AddMessage(" ")  
arcpy.AddMessage("> Finished...")
arcpy.AddMessage(" ")  
