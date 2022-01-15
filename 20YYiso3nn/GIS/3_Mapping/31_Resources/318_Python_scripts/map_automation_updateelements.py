""" This scripts brings together all data and maps for the report """
import os
#import string
#import shutil
#from shutil import copyfile

################################################################################
# Manipulating the maps so data is loaded, displayed and scaled correctly
def main(origtemp, elemdict, mxdList, mxdsout, mapnumb,
         versnum, resppais, respglid, respprod):

# Setting up variables
    sep = os.path.sep

# This does the element changing of text, location and legend image
    for elemtype in range(len(elemdict)):
        if origtemp == elemdict[elemtype]['temp'][0]:
            for mxdFile in mxdList:
                mxdlocation = mxdsout + mapnumb + sep + mxdFile
                print mxdlocation
                mxds = arcpy.mapping.MapDocument(mxdlocation)
                for elem in arcpy.mapping.ListLayoutElements(mxds, ""):
                    if elem.name == "legend_jpg":
                        newImage = legedir + "ma" + mxdFile[3:6] + "_" + origtemp + ".jpg"
                        print newImage
                        elem.sourceImage = newImage
                        elem.elementPositionX = elemdict[elemtype]['cenx'][0]
                        elem.elementPositionY = elemdict[elemtype]['ceny'][0]
                    if elem.name == "map_no":
                        elem.text = "MA" + mapnumb[-3:] + " " + versnum
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
