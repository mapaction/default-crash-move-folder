""" This scripts brings together all data and maps for the report """
import os
#import string
import shutil
from shutil import copyfile

################################################################################
# Manipulating the maps so data is loaded, displayed and scaled correctly
def main(absroot, mapsdir, origmap, origtemp, mapsdict):

# Setting up variables
    sep = os.path.sep
    count = 1

# Directory location details
    mapsdir = absroot + sep + "3_Mapping" + sep
    mxdsdir = mapsdir + "32_Map_Templates" + sep
#    origmap = mxdsdir + "arcmap-10.6_reference_" + origtemp + ".mxd"
    mxdsout = mapsdir + "33_Map_Projects" + sep
    jpgsout = mapsdir + "34_Map_Products_MapAction" + sep

# This makes the directories if they don't exist
    for mapstype in range(len(mapsdict)):
        versnum = "v0" + str(count)
        mapnumb = mapsdict[mapstype]['code'][0]
#        missingdata = []
        print "Working on map: " + mapnumb
        mapdirs = mxdsout + mapnumb
        outdirs = jpgsout + mapnumb
        dirstocreate = [mapdirs, outdirs]
        for directories in dirstocreate:
            if not os.path.exists(directories):
                try:
                    os.makedirs(directories)
                except:
                    print "1 Failed to make " + directories
        for root, dirs, files in os.walk(mapdirs):
            for filez in files:
                splitfilez = filez.split("-")
                if int(splitfilez[1][-1:]) == 9:
                    deccount = int(splitfilez[1][-2:-1]) + 1
                    versnum = "v" + str(deccount) + "0"
                else:
                    versnum = splitfilez[1][:-1] + str((int(splitfilez[1][-1:]) + 1))
                if not os.path.exists(os.path.join(outdirs, versnum)):
                    try:
                        os.makedirs(os.path.join(outdirs, versnum))
                    except:
                        print "2 Failed to make " + outdirs + sep + versnum
        finalmap = mxdsout + mapnumb + sep + mapnumb + "-" + \
                   versnum + "-" + mapsdict[mapstype]['maps'][0]

        copyfile(origmap, finalmap)
        mapminusext = jpgsout + mapnumb + sep + versnum + \
                      sep + mapnumb + "-" + versnum + "-" + \
                      mapsdict[mapstype]['maps'][0][:-4]
        finaljpg = mapminusext + ".jpg"
        if not os.path.exists(os.path.join(outdirs, versnum)):
            try:
                os.makedirs(os.path.join(outdirs, versnum))
            except:
                print "3 Failed to make " + outdirs + sep + versnum

    return finaljpg