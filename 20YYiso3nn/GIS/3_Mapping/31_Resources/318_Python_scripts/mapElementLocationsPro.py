import os
import arcpy
from datetime import date

def getAprxFiles(directory):
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
    file = os.path.join(os.getcwd(), '20YYiso3nn', 'GIS','3_Mapping', '32_Map_Templates', "template_positions_" + today + ".txt")
    return open(file, 'a+')

def createMapTemplateLocations():
    crashMoveDirectory = os.getcwd()
    arcpy.env.workspace = crashMoveDirectory

    writeOutputFileHeadings()

    for aprxFile in getAprxFiles(crashMoveDirectory):     
        getLayoutsInAPRXFile(aprxFile)
    
createMapTemplateLocations()
 
