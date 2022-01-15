""" This scripts brings together all data and maps for the report """
import os
import time
import arcpy
from arcpy import env
import string
import shutil
from shutil import copyfile
import map_automation_addtomap

################################################################################
# Manipulating the maps so data is loaded, displayed and scaled correctly
def main(origmaps, origtemp, absroot, respdict,
         datadict, mapsdict, elemdict, framdict):

# Setting up variables
    count = 1
    datasources = []
# Response details
    for resplist in range(len(respdict)):
        resppais = str(respdict[resplist]['pais'][0])
        respiso3 = str(respdict[resplist]['iso3'][0])
        respglid = str(respdict[resplist]['glid'][0])
        respsupp = str(respdict[resplist]['supp'][0])
        respzone = str(respdict[resplist]['zone'][0])
        respprod = str(respdict[resplist]['prod'][0])
    sep = os.path.sep

# Frame scaling details
    for framlist in range(len(framdict)):
        if framdict[framlist]['fram'][0] == "Main map":
            frammain = str(framdict[framlist]['data'][0])
        elif framdict[framlist]['fram'][0] == "Location map":
            framloca = str(framdict[framlist]['data'][0])
        else:
            print "No scaling data"
  
# Directory location details
    datadir = absroot + sep + "2_Active_Data" + sep
    mapsdir = absroot + sep + "3_Mapping" + sep
    mxdsout = mapsdir + "33_Map_Projects" + sep
    jpgsout = mapsdir + "34_Map_Products_MapAction" + sep
    symbdir = mapsdir + "31_Resources" + sep + "312_Layer_files" + sep
    legedir = mapsdir + "31_Resources" + sep + "317_Legends" + sep

# Date and time details
    gentime = time.strftime('%H:%M')
    gendate = time.strftime('%d %b %Y')
    
# This makes the directories if they don't exist
    for mapstype in range(len(mapsdict)):
        versnum = "v0" + str(count)
        mapnumb = mapsdict[mapstype]['code'][0]
        missingdata = []
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

        copyfile(origmaps, finalmap)
        mapminusext = jpgsout + mapnumb + sep + versnum + \
                      sep + mapnumb + "-" + versnum + "-" + \
                      mapsdict[mapstype]['maps'][0][:-4]
        finaljpg = mapminusext + ".jpg"
        if not os.path.exists(os.path.join(outdirs, versnum)):
            try:
                os.makedirs(os.path.join(outdirs, versnum))
            except:
                print "3 Failed to make " + outdirs + sep + versnum

# This does the adding and swapping of datasourses
        mxds = arcpy.mapping.MapDocument(finalmap)
        for df in arcpy.mapping.ListDataFrames(mxds, "*"):
            dataframe = df.name
            for mapslist in range(len(mapsdict[mapstype]['main'])):
                mapsvar = mapsdict[mapstype]['main'][mapslist]
                for datalist in range(len(datadict)):
                    if dataframe == datadict[datalist]['fram'][0]:
                        if mapsvar == datadict[datalist]['lyrs'][0]:
                            arcpy.env.workspace = datadir + datadict[datalist]['dirs'][0]
                            if datadict[datalist]['iso3'][0] == "reg":
                                fcwildcard = "reg" + datadict[datalist]['name'][0]
                            else:
                                fcwildcard = respiso3 + \
                                             datadict[datalist]['name'][0]
                            splittype = fcwildcard.split("_")
                            if splittype[3] == "ras":
                                dataclasses = arcpy.ListRasters(fcwildcard)
                            else:
                                dataclasses = arcpy.ListFeatureClasses(fcwildcard)
                            listcount = 0
                            datatoswap = ""
                            if len(dataclasses) >= 2:
                                choosedata = ""
                                for data in dataclasses:
                                    splitdata = data.split("_")
                                    if splitdata[5] == respsupp:
                                        datatoswap = data
                                    else:
                                        choosedata = choosedata + str("  {}: {}\n".format(listcount + 1, data))
                                        listcount += 1
                                check = False

                                if len(datatoswap) == 0:
#                                    print " Enter data to be used in automation maps: "
                                    question = " Choose from possible datasets to match\n  '" + mapsvar + "': "
                                    print choosedata,
                                    while check is False:
                                        try:
                                            data_idx = int((raw_input(question)))
                                            if data_idx >= (len(dataclasses) + 1) or data_idx == 0:
                                                print " Try again, you entered a non viable number"
                                            else:
                                                datatoswap = dataclasses[data_idx - 1]
                                                check = True
                                        except ValueError:
                                            print " Try again, you entered more than one option or text"
                            if len(dataclasses) == 1:
                                if datadict[datalist]['iso3'][0] == "reg":
                                    datatoswap = dataclasses[0]
                                else:
                                    datatoswap = datadict[datalist]['iso3'][0] + dataclasses[0]

                            # not great but to catch if no data present
                            if len(dataclasses) == 0:
                                missingdata.append(datadict[datalist]['lyrs'][0] + "\n")
                            elif os.path.exists(symbdir + datadict[datalist]['lyrs'][0] + ".lyr"):
                                splitlist = datatoswap.split("_")
                                datasources.append(splitlist[5])
                                if arcpy.Exists(datatoswap):
                                    map_automation_addtomap.load(symbdir, datadict[datalist]['fram'][0],
                                                                 datadict[datalist]['lyrs'][0], df)
                                    map_automation_addtomap.swap(mapsvar, datadict[datalist]['fram'][0],
                                                                 datadir + datadict[datalist]['dirs'][0],
                                                                 df, mxds, datatoswap)
                            else:
                                print datadict[datalist]['lyrs'][0] + ".lyr doesn't exist"
        
        mxds.save()

        missingset = set(missingdata)
        datamissing = "The following lyr files have no data for map " + mapnumb + " :\n "
        misscount = 0
        for datamiss in missingset:
            datamissing = datamissing + datamiss + "\n "
            misscount += 1
        if misscount >= 1:
            print datamissing[:-2]

        myset = set(datasources)
        mapdatasources = ""
        for datasets in myset: 
            mapdatasources = mapdatasources + datasets + ", "
        mxds.save()

# This does the scaling of the map
        df = arcpy.mapping.ListDataFrames(mxds, "Location map")[0]
        for localyr in arcpy.mapping.ListLayers(mxds, framloca, df):
            if mapnumb == "MA8006":
                scalemultiple = 1
            else:
                scalemultiple = 1.5
            arcpy.SelectLayerByAttribute_management(localyr)
            df.zoomToSelectedFeatures()
            scale = round(df.scale, -3)
            df.scale = scale * scalemultiple
            arcpy.RefreshActiveView()
            arcpy.SelectLayerByAttribute_management(localyr, "CLEAR_SELECTION")

        df = arcpy.mapping.ListDataFrames(mxds, "Main map")[0]
        for mainlyr in arcpy.mapping.ListLayers(mxds, frammain, df):
            arcpy.SelectLayerByAttribute_management(mainlyr)
            df.zoomToSelectedFeatures()
            df.scale = round(df.scale, -3)
            arcpy.RefreshActiveView()
            arcpy.SelectLayerByAttribute_management(mainlyr, "CLEAR_SELECTION")

        mxds.save()

# This does the element changing of text, location and legend image
        for elemtype in range(len(elemdict)):
            if origtemp == elemdict[elemtype]['temp'][0]:
                mxds = arcpy.mapping.MapDocument(finalmap)
                for elem in arcpy.mapping.ListLayoutElements(mxds, ""):
                    if elem.name == "legend_jpg":
                        newImage = legedir + "ma" + mapnumb[-3:] + "_" + origtemp + ".jpg"
                        elem.sourceImage = newImage
                        elem.elementPositionX = elemdict[elemtype]['cenx'][0]
                        elem.elementPositionY = elemdict[elemtype]['ceny'][0]
                    if elem.name == "map_no":
                        elem.text = "MA" + mapnumb[-3:] + " " + versnum
                    if elem.name == "time_zone":
                        elem.text = respzone
                    if elem.name == "data_sources":
                        elem.text = mapdatasources[:-1]
                    if elem.name == "country":
                        elem.text = resppais
                    if elem.name == "create_date_time":
                        elem.text = str(gendate) + " / " + str(gentime)
                    if elem.name == "glide_no":
                        elem.text = respglid
                    if elem.name == "map_producer":
                        elem.text = respprod
                    if elem.name == "title":
                        elem.text = str(mapsdict[mapstype]['titl'][0])
                    if elem.name == "summary":
                        elem.text = str(mapsdict[mapstype]['summ'][0])

        try:
            print "Exporting jpg maps for " + str(mapnumb) + " " + versnum + "\n"
            arcpy.mapping.ExportToJPEG(mxds, finaljpg, resolution = "200")
##            arcpy.mapping.ExportToPDF(mxds, finalpdf, resolution = "200")
##            arcpy.mapping.ExportToPNG(mxds, finalpng, resolution = "200")
        except:
            print str(mapnumb) + " " + versnum + " not exported"

        mxds.save()
