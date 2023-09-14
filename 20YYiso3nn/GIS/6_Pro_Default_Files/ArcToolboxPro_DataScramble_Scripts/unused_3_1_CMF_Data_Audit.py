#----------------------------------------------------------------------------#
# Poll the Active Directory folder.
# Author:   MapAction Team Bravo (James Wharfe)
# Date:     2019.06.08 - Adapted 2021.03.28 for RDSP (Tom Hughes)
# 
#----------------------------------------------------------------------------#

import os
import csv
import pandas as pd
import pdb
import xlwt
from datetime import datetime

# Get date/time for output docs
now = datetime.now()
dt_string = now.strftime("%y%m%d_%H%M")

# Get Path to CMF
#cmf = r'G:\Shared drives\prepared-country-data\fiji'
cmf = arcpy.GetParameterAsText(0)
arcpy.AddMessage("> CMF = " + cmf)
arcpy.AddMessage(" ")

# Check the lookups folder for nice names
def get_lookup(value, index):
    lookupDir = os.path.join(cmf, r'GIS\2_Active_Data\200_data_name_lookup')
    index = '0{0}'.format(index)
    files = []
    for r, d, f in os.walk(lookupDir):
        for file in f:
            if '.csv' in file:
                # We don't wan't the last file '99_DNCmetadata' since the
                # format is different to the other files
                if file == '99_DNCmetadata.csv': continue
                files.append(os.path.join(r, file))
    # Should load up the specific index but can also lookup against all
    # of them.
    dictList = []
    results = []
    for fpath in files:
        #print(fpath)
        data = pd.read_csv(fpath)
        #arcpy.AddMessage(data)
        #arcpy.AddMessage("Reading: " + fpath)
        # Check lookup
        # Massive assumptions made about the structure of the Lookup files.
        # This needs to be fixed/cleaned/refactored etc.
        # - Always includes the first column 'Value'
        # - An accurate description of the key in present in the second column
        lookup = data[data['Value'].isin([value])]
        if len(lookup) > 0:
            lookup_value = lookup.iloc[:, 1:2]
            #print(lookup_value['Description'].values[0])
            #arcpy.AddMessage("  > Description: " + lookup_value)
            try:
                #results.append(lookup_value['Description'][1])
                results.append(lookup_value['Description'].values[0])
            except Exception, err:
                print('Error: {0}'.format(err))
                arcpy.AddMessage('Error: {0}'.format(err))
                pdb.set_trace()
    # Return results
    if len(results) == 0:
        #print('\tno lookup found for \'{0}\''.format(value))
        arcpy.AddMessage("   > no lookup value found for "'{0}\''.format(value))
        return value
    elif len(results) > 1:
        #print('\tmultiple lookups found for \'{0}\''.format(results))
        arcpy.AddMessage("   > Multiple lookup values found for " '{0}\''.format(results))
        return value
    else:
        #print('Lookup found')
        return results[0]


def parse_named_source_file(fname):
    print('Parsing {0}'.format(fname))
    arcpy.AddMessage("Parsing " '{0}'.format(fname))
    file_name, ext = os.path.splitext(fname)
    parts = file_name.split('_')
    sectionDict = {
            0: r'geoextent',
            1: r'catetory',
            2: r'theme',
            3: r'geometry',
            4: r'scale',
            5: r'source',
            6: r'permission',   # Ignored in this first pass
            7: r'DNCmetadata'   # Ignored in this first pass
            }
    if len(parts) < 6:
        print('\tnon standard formatted data')
        arcpy.AddMessage("   > Non standard formatted data")
        print('\tnot processing.')
        arcpy.AddMessage("   > Not processing")        
        return "", "", "", "", "", ""
    #arcpy.AddMessage("   > parse_named_source_file function: " + fname)   
    geoextent = get_lookup(parts[0], 0)
    #arcpy.AddMessage("   > " + geoextent)
    category = get_lookup(parts[1], 1)
    #arcpy.AddMessage("   > " + category)
    theme = get_lookup(parts[2], 2)
    #arcpy.AddMessage("   > " + theme)
    geometry = get_lookup(parts[3], 3)
    #arcpy.AddMessage("   > " + geometry)
    scale = get_lookup(parts[4], 4)
    #arcpy.AddMessage("   > " + scale)
    source = get_lookup(parts[5], 5)
    #arcpy.AddMessage("   > " + source)
    return geoextent, category, theme, geometry, scale, source


def parse_directory(sourceDir, extList):
    sourceList = []
    filecountList = [] ###
    for root, dirs, files in os.walk(sourceDir):
        # Quick hack to exclude the '200_data_name_lookup' files
        ignore = os.path.join(cmf, r'GIS\2_Active_Data\200_data_name_lookup')
        if root == ignore:
            continue
        for file in files:
            for ext in extList:
                if file.endswith(ext):
                    #print(os.path.join(root, file))
                    sourceList.append([root, file])
    return sourceList

def parse_origdata(origDir, extList):
    origList = []
    #arcpy.AddMessage(origDir)
    for root, dirs, files in os.walk(origDir):
        for file in files:
            for ext in extList:
                if file.endswith(ext):
                    origList.append([root, file])
    return origList

def count_files(sourceDir, extList): 
    subfolderCounts = []
    folders = next(os.walk(sourceDir))[1]
    for folder in folders:
        filecountList = []
        files = []
        dirList = []
        pathtocount = os.path.join(sourceDir, folder)
        files = os.listdir(pathtocount)
        for file in files:
            if os.path.isdir(os.path.join(sourceDir, folder,file)):
                dirList.append(file)
            else: 
                for ext in extList:
                    if file.endswith(ext):
                        if file != 'enable-empty-dir-in-github.txt':
                            #arcpy.AddMessage(file)
                            filecountList.append(file)
        c_files = len(filecountList)
        c_dirs = len(dirList)
        #arcpy.AddMessage(folder + ": " + str(c_files) + ": " + str(c_dirs))
        subfolderCounts.append([folder, c_files, c_dirs])   
    return subfolderCounts
    
def main():
    # Parse Activated Data directory
    sourceDir = os.path.join(cmf, r'GIS\2_Active_Data')
    origDir = os.path.join(cmf, r'GIS\1_Original_Data')
    extList = [".csv", ".txt", ".shp", ".xlsx", ".tif", ".img"]
    #extList = [".txt", ".shp", ".xlsx", ".tif", ".img"]
    
    sourceList = parse_directory(sourceDir, extList)
    subfolderCounts = count_files(sourceDir, extList)
    origList = parse_origdata(origDir, extList)  
    
    # Add to Pandas dataframe
    df = pd.DataFrame(sourceList)
    df.columns = ['Path', 'Filename']
    df.sort_values(by=['Path'],ascending=True,inplace=True)

    df2 = pd.DataFrame(subfolderCounts)
    df2.columns = ['Folder_name','Datasets','SubFolders']
    df2.sort_values(by=['Folder_name'],ascending=True,inplace=True)
    
    if len(origList) > 0:
        df3 = pd.DataFrame(origList)
        df3.columns = ['Path', 'Filename']
        df3.sort_values(by=['Path'],ascending=True,inplace=True)

    # Skip 'enable-empty-dir-in-github.txt' type files
    df.drop(df[df['Filename'] == r'enable-empty-dir-in-github.txt'].index, inplace=True)

    # Further parse the file name (makes assumptions about the name)
    # ie. Should be activated in line with the data naming tool.
    df['geoextent'], df['category'], df['theme'], df['geometry'], df['scale'], df['source'] = zip(*df['Filename'].map(parse_named_source_file))
   
   # Output results
    outname = 'Data_Audit_' + dt_string
    #df.to_csv(cmf + os.sep + outname + '.csv', index=False)
    
    with pd.ExcelWriter(cmf + os.sep + outname + '.xls') as writer:
        if len(origList) > 0:
            df3.to_excel(writer, sheet_name='1_Original_Data',index=False)    
        df.to_excel(writer, sheet_name='2_Active_Data',index=False)
        df2.to_excel(writer, sheet_name='2_Active_Data_Counts',index=False)

    arcpy.AddMessage(" ")
    arcpy.AddMessage("Finished. Check CMF for outputs: ")
    #arcpy.AddMessage("   > " + cmf + os.sep + outname + ".csv")
    arcpy.AddMessage("   > " + cmf + os.sep + outname + ".xls")
    arcpy.AddMessage(" ")
    
if __name__ == '__main__':
    main()
