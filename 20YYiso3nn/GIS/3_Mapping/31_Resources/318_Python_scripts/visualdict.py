import os
import sys
# These are required for DConnaghan MapAction laptop-91 as some strange python settings
sys.path.append("C:\\python27\\ArcGIS10.8\\Lib\\site-packages")
sys.path.append(r"C:\Program Files (x86)\ArcGIS\Desktop10.8\arcpy")
sys.path.append(r"C:\Program Files (x86)\ArcGIS\Desktop10.8\ArcToolbox\Scripts")
sys.path.append(r"C:\Program Files (x86)\ArcGIS\Desktop10.8\bin")
sys.path.append("C:\\python27\\ArcGIS10.8\\Lib")
import arcpy
import datetime

# =============================================================================
# Runs through dictionary items
# =============================================================================

# Luis, can you comment this please
def main(dictionary):
    """Prints all pairs of keys and value of a dict"""
    for key, value in sorted(dictionary.items()):
        print(key, value)

    return key, value