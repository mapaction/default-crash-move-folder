import os
import sys
import glob
# These are required for DConnaghan ma-laptop-92 as some strange python settings
# sys.path.append('C:\\python27\\ArcGIS10.8\\Lib\\site-packages')
# sys.path.append(r'C:\Program Files (x86)\ArcGIS\Desktop10.8\arcpy')
# sys.path.append(r'C:\Program Files (x86)\ArcGIS\Desktop10.8\ArcToolbox\Scripts')
# sys.path.append(r'C:\Program Files (x86)\ArcGIS\Desktop10.8\bin')
# sys.path.append('C:\\python27\\ArcGIS10.8\\Lib')
import arcpy

# =============================================================================
# Global variables
# =============================================================================
def main():

    sep = os.path.sep
    crs_error = []

    arr_folder  = ['202_admn', '215_heal', '229_stle', '232_tran']
    # add here any point datasets that should have an admin PCode values applied
    # dictionary to be used in applycorrectfieldnames.py
    fold_names  = {'*_admn_*': '202_admn',
                   '*_heal_*': '215_heal',
                   '*_stle_*': '229_stle',
                   '*_tran_*': '232_tran'}

    # required fields for automation labelling and symbology
    admn_names  = {'0n': 'adm_0',
                  '1n': 'ADM1_EN',
                  '1p': 'ADM1_PCode',
                  '2n': 'ADM2_EN',
                  '2p': 'ADM2_PCode',
                  '3n': 'ADM3_EN',
                  '3p': 'ADM3_PCode',
                  '4n': 'ADM4_EN',
                  '4p': 'ADM4_PCode'}
    # add here any field names that should exist for settlements
    stle_names  = {'stle_type': 'fclass',
                   'stle_name': 'name'}
    # add here any field names that should exist for airports
    airp_names  = {'airp_type': 'type',
                   'airp_name': 'name'}
    # add here any field names that should exist for ports
    port_names  = {'port_name': 'PORT_NAME'}
    # add here any field names that should exist for health facilities
    heal_names  = {'heal_type': 'fclass',
                   'heal_name': 'name'}

    # setting the main directory
    python_dir = os.getcwd()
    # main admn_dir - will be used in different .py
    admn_dir = python_dir + '/' + '202_admn'
    display_split = '-------------------------'

    
    return sep, crs_error, arr_folder, fold_names, admn_names, stle_names, airp_names, port_names, heal_names, python_dir, admn_dir, display_split
