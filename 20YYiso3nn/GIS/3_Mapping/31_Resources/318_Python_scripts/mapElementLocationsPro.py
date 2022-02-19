import os
import arcpy
import re
from datetime import date

delimiter = '|';

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
        outputFile.write(delimiter.join(elements))
        outputFile.write('\n')
        outputFile.close()
        
def removeAPRXVersionNumber(aprxFileName):
    nameParts = aprxFileName.split('_')
    return '-'.join(nameParts[2:])

def isString(element):
    return isinstance(element, str)

def formatString(element): 
    markupRegex = re.compile('<.*?>') 
    if isString(element):
        strippedMarkup = re.sub(markupRegex, '', element)
        return strippedMarkup.replace(delimiter, ' ').replace('\n',' ').encode('ascii', errors='ignore').decode()
    else:
        return element


def lookForElements(layout, aprxFileName):
    with writeToOutputFile() as outputFile:
        print(removeAPRXVersionNumber(aprxFileName[:-5]))
        for element in layout.listElements(wildcard='*'):
            elementFragments = []
            elementFragments.append(str(removeAPRXVersionNumber(aprxFileName[:-5])))
            elementFragments.append(str(formatString(layout.name))) 
            elementFragments.append(str(formatString(element.name))) 
            elementFragments.append(str(formatString(element.type)))
            elementFragments.append(str(formatString(element.elementPositionX)))
            elementFragments.append(str(formatString(element.elementPositionY)))
            elementFragments.append(str(formatString(element.elementHeight)))
            elementFragments.append(str(formatString(element.elementWidth)))

            if element.type == 'TEXT_ELEMENT':
                elementFragments.append(str(formatString(element.textSize)))
                elementFragments.append(str(formatString(element.text)))
        
            outputFile.write(delimiter.join(elementFragments))
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