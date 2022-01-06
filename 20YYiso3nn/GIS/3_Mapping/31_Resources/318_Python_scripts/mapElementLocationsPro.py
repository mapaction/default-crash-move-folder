import os
import sys
sys.path.append("C:\\py27arcgis106\\ArcGIS10.6\\Lib\\site-packages")
sys.path.append(r'C:\Program Files (x86)\ArcGIS\Desktop10.6\arcpy')
sys.path.append(r'C:\Program Files (x86)\ArcGIS\Desktop10.6\ArcToolbox\Scripts')
sys.path.append(r'C:\Program Files (x86)\ArcGIS\Desktop10.6\bin')
sys.path.append("C:\\py27arcgis106\\ArcGIS10.6\\Lib")
import arcpy
from arcpy import env
from datetime import date

def getAprxFiles(directory):
    print "directory: " + directory
    aprxFiles = [];
    for root, dirs, files, in os.walk(directory):
        for file in files:
            if file.endswith(".aprx"):
                aprxFiles.append(os.path.join(root, file))
    return aprxFiles

def getLayoutsInAPRXFile(aprxFile):
    aprx = arcpy.mp.ArcGISProject(aprxFile)

    aprxFileName = aprxFile.split(os.path.sep)[-1]
    layouts = aprx.listLayouts()

    for layout in layouts:
        lookForElements(layout, aprxFileName)

def writeOutputFileHeadings():
    elements = ['APRXFile', 'LayoutName', 'MapName', 'Type', 'ElementName', 'PositionX', 'PositionY', 'Height', 'Width', 'FontSize', 'TextValue']
    with writeToOutputFile() as outputFile:
        outputFile.write(','.join(elements))
        outputFile.write('\n')
        outputFile.close()
        

def lookForElements(layout, aprxFileName):
    with writeToOutputFile() as outputFile:
    
        for element in layout.listElements(wildcard='*'):
            elementFragments = []
            elementFragments.append(aprxFileName)
            elementFragments.append(layout.name) 
            elementFragments.append(str(element.name)) 
            elementFragments.append(str(element.type)) 
            elementFragments.append(str(element.elementPositionX))
            elementFragments.append(str(element.elementPositionY)) 
            elementFragments.append(str(element.elementHeight))
            elementFragments.append(str(element.elementWidth))

            if element.type == 'TEXT_ELEMENT':
                elementFragments.append(str(element.textSize))
                elementFragments.append(str(element.text))
        
            outputFile.write(','.join(elementFragments))
            outputFile.write('\n')
        

def writeToOutputFile():
    today = str(date.today())
    root = os.getcwd()
    print root[:-31]
    file = os.path.join(root[:-31], '32_Map_Templates', "template_positions_" + today + ".txt")
    return open(file, 'a+')

def createMapTemplateLocations():
    crashMoveDirectory = os.getcwd()
    print "crashMoveDirectory: " + crashMoveDirectory[:-31]
    arcpy.env.workspace = crashMoveDirectory[:-31]

    writeOutputFileHeadings()

    for aprxFile in getAprxFiles(crashMoveDirectory[:-31]):
        print aprxFile
        getLayoutsInAPRXFile(aprxFile)
    
createMapTemplateLocations()
 
