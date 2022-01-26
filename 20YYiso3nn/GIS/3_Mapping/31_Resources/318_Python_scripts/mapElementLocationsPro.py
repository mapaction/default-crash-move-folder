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
   elements = ['TemplateName', 'LayoutName', 'ElementName', 'Type', 'PositionX', 'PositionY', 'Height', 'Width', 'FontSize', 'TextValue']
   with writeToOutputFile() as outputFile:
        outputFile.write(','.join(elements))
        outputFile.write('\n')
        outputFile.close()

def wrapElementInQuotes(value):
    return '"{}"'.format(str(value))

def removeAPRXVersionNumber(aprxFileName):
    nameParts = aprxFileName.split('_')
    return '-'.join(nameParts[2:])

def lookForElements(layout, aprxFileName):
    with writeToOutputFile() as outputFile:
        print(removeAPRXVersionNumber(aprxFileName[:-5]))
        for element in layout.listElements(wildcard='*'):
            elementFragments = []
            elementFragments.append(wrapElementInQuotes(removeAPRXVersionNumber(aprxFileName[:-5])))
            elementFragments.append(wrapElementInQuotes(layout.name)) 
            elementFragments.append(wrapElementInQuotes(element.name)) 
            elementFragments.append(wrapElementInQuotes(element.type)) 
            elementFragments.append(wrapElementInQuotes(element.elementPositionX))
            elementFragments.append(wrapElementInQuotes(element.elementPositionY)) 
            elementFragments.append(wrapElementInQuotes(element.elementHeight))
            elementFragments.append(wrapElementInQuotes(element.elementWidth))

            if element.type == 'TEXT_ELEMENT':
                elementFragments.append(wrapElementInQuotes(element.textSize))
                elementFragments.append(wrapElementInQuotes(element.text))

            outputFile.write(','.join(elementFragments))
            outputFile.write('\n')
        
def writeToOutputFile():
    today = str(date.today())
    file = os.path.join(os.getcwd(), '20YYiso3nn', 'GIS','3_Mapping', '32_Map_Templates', '325_Misc', '3253_element-locations', "template_positions_" + today + ".txt")
    return open(file, 'a+')

def createMapTemplateLocations():
    crashMoveDirectory = os.getcwd()
    arcpy.env.workspace = crashMoveDirectory

    writeOutputFileHeadings()

    for aprxFile in getAprxFiles(crashMoveDirectory):     
        getLayoutsInAPRXFile(aprxFile)
    
createMapTemplateLocations()
 