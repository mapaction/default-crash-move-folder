""" This script automatically generates standard maps """
# ---------------------------------------------------------------------------
# main_reportbody_server.py
# only runs with python from C:\Python27\ArcGIS10.2
# ---------------------------------------------------------------------------

import os
import sys
sys.path.append("C:\\py27arcgis106\\ArcGIS10.6\\Lib\\site-packages")
sys.path.append("C:\\Program Files (x86)\\ArcGIS\\Desktop10.6\\arcpy")
sys.path.append("C:\\Program Files (x86)\\ArcGIS\\Desktop10.6\\ArcToolbox\\Scripts")
sys.path.append("C:\\Program Files (x86)\\ArcGIS\\Desktop10.6\\bin")
sys.path.append("C:\\py27arcgis106\\ArcGIS10.6\\Lib")
import time
import datetime

import map_automation_ratio
import map_automation_makedirs
import map_automation_buildmaps
import map_automation_configsettings

################################################################################
def runreports():
    """ Runs reports based on numbers below """

    # get this files directory to check if running test or live reports
    sep = os.path.sep
    appdir = os.getcwd()
    absroot = appdir[:-42]

    # dictionaries holding the data, maps, report and page config details
    (respdict) = map_automation_configsettings.respconfig()
    (datadict) = map_automation_configsettings.dataconfig()
    (mapsdict) = map_automation_configsettings.mapsconfig()
    (elemdict) = map_automation_configsettings.elemconfig()
    (framdict) = map_automation_configsettings.framconfig()

    for resplist in range(len(respdict)):
        resppais = str(respdict[resplist]['pais'][0])

    screentext = "\n" + time.strftime('%H:%M:%S') + \
                 " Starting to generate automated maps for '" + resppais + "'"
    print(screentext)

    origmaps, origtemp = map_automation_ratio.main(absroot, respdict, datadict)
    map_automation_buildmaps.main(origmaps, origtemp, absroot, respdict,
                                  datadict, mapsdict, elemdict, framdict)

    screentext = "\n" + time.strftime('%H:%M:%S') + \
                 " Ending generation of automated maps"
    print(screentext)
    del absroot, respdict, datadict, mapsdict, elemdict, framdict

################################################################################
if __name__ == "__main__":

    runreports()
    
    sys.exit()
