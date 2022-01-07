""" This script returns the various config settings for reports, search
radii, maps and anything else that is centrally managed """
# ------------------------------------------------------------------------------
# siteanalysis_configsettings.py
# ------------------------------------------------------------------------------

import os

################################################################################
# Returns the configuration settings for the report generation
def respconfig():

    respdict = [
                {'pais':["Mozambique"],
                 'iso3':["moz"],
                 'glid':["XX-2021-nnnnnn-MOZ"],
                 'supp':["ine"],
                 'zone':["UTC 1 1"],
                 'prod':["Produced by MapAction mapaction.org mozambique@mapaction.org"]}
               ]
    # Return the resp (response) dictionary
    return respdict

################################################################################
# Returns the configuration settings for the report generation
def mapsconfig():

    mapsdict = [
                {'code':["MA8001"],
                 'maps':["country-overview-with-admin1-and-boundaries.mxd"],
                 'titl':["Country Overview with Admin 1 Boundaries and Topography"],
                 'summ':["Country overview with topography displayed"],
                 'temp':["reference"],
                 'main':["mainmap-admn-ad0-py-s0-scaling",
                         "mainmap-stle-stl-pt-s0-allmaps",
                         "mainmap-tran-air-pt-s0-allmaps",
                         "mainmap-tran-por-pt-s0-allmaps",
                         "mainmap-elev-cst-ln-s0-allmaps",
                         "mainmap-admn-ad0-ln-s0-reference",
                         "mainmap-admn-ad1-ln-s0-reference",
                         "mainmap-phys-riv-ln-s0-reference",
                         "mainmap-phys-wat-py-s0-allmaps",
                         "mainmap-elev-dem-ras-s0-reference",
                         "mainmap-elev-hsh-ras-s0-reference",
                         "mainmap-admn-ad0-ln-s0-surroundingcountries",
                         "mainmap-admn-ad1-py-s0-reference",
                         "mainmap-carto-fea-py-s0-allmaps",
                         "mainmap-admn-ad0-py-s0-surroundingcountries",
                         "locationmap-carto-fea-py-s0-reference",
                         "locationmap-elev-cst-ln-s0-reference",
                         "locationmap-admn-ad0-ln-s0-surroundingcountries",
                         "locationmap-admn-ad0-py-s0-scaling",
                         "locationmap-admn-ad0-py-s0-surroundingcountries"]},
                {'code':["MA8002"],
                 'maps':["country-overview-with-admin1-boundaries.mxd"],
                 'titl':["Country Overview with Admin 1 Boundaries"],
                 'summ':["Country overview with detail of Admin 1 boundaries and major cities"],
                 'temp':["reference"],
                 'main':["mainmap-admn-ad0-py-s0-scaling",
                         "mainmap-elev-cst-ln-s0-allmaps",
                         "mainmap-admn-ad0-ln-s0-reference",
                         "mainmap-admn-ad1-ln-s0-reference",
                         "mainmap-admn-ad0-ln-s0-surroundingcountries",
                         "mainmap-admn-ad1-py-s0-reference",
                         "mainmap-carto-fea-py-s0-allmaps",
                         "mainmap-admn-ad0-py-s0-surroundingcountries",
                         "locationmap-carto-fea-py-s0-reference",
                         "locationmap-elev-cst-ln-s0-reference",
                         "locationmap-admn-ad0-ln-s0-surroundingcountries",
                         "locationmap-admn-ad0-py-s0-scaling",
                         "locationmap-admn-ad0-py-s0-surroundingcountries"]},
                {'code':["MA8003"],
                 'maps':["country-overview-with-admin1-boundaries-and-cities.mxd"],
                 'titl':["Country Overview with Admin 1 Boundaries"],
                 'summ':["Country overview with detail of Admin 1 boundaries and major cities"],
                 'temp':["reference"],
                 'main':["mainmap-admn-ad0-py-s0-scaling",
                         "mainmap-stle-stl-pt-s0-allmaps",
                         "mainmap-elev-cst-ln-s0-allmaps",
                         "mainmap-admn-ad0-ln-s0-reference",
                         "mainmap-admn-ad1-ln-s0-reference",
                         "mainmap-admn-ad2-ln-s1-reference",
                         "mainmap-admn-ad0-ln-s0-surroundingcountries",
                         "mainmap-admn-ad1-py-s0-reference",
                         "mainmap-admn-ad2-py-s1-reference",
                         "mainmap-carto-fea-py-s0-allmaps",
                         "mainmap-admn-ad0-py-s0-surroundingcountries",
                         "locationmap-carto-fea-py-s0-reference",
                         "locationmap-elev-cst-ln-s0-reference",
                         "locationmap-admn-ad0-ln-s0-surroundingcountries",
                         "locationmap-admn-ad0-py-s0-scaling",
                         "locationmap-admn-ad0-py-s0-surroundingcountries"]},
                {'code':["MA8004"],
                 'maps':["country-overview-with-transport.mxd"],
                 'titl':["Country Overview with Transport"],
                 'summ':["Shows country overview with transport information such as airports and ports"],
                 'temp':["reference"],
                 'main':["mainmap-admn-ad0-py-s0-scaling",
                         "mainmap-stle-stl-pt-s0-allmaps",
                         "mainmap-elev-cst-ln-s0-allmaps",
                         "mainmap-admn-ad0-ln-s0-reference",
                         "mainmap-tran-por-pt-s0-allmaps",
                         "mainmap-tran-por-pt-s0-allmaps",
                         "mainmap-admn-ad1-ln-s0-reference",
                         "mainmap-tran-rds-ln-s0-allmaps",
                         "mainmap-tran-rrd-ln-s0-allmaps",
                         "mainmap-phys-wat-py-s0-allmaps",
                         "mainmap-admn-ad0-ln-s0-surroundingcountries",
                         "mainmap-admn-ad1-py-s0-reference",
                         "mainmap-carto-fea-py-s0-allmaps",
                         "mainmap-admn-ad0-py-s0-surroundingcountries",
                         "locationmap-carto-fea-py-s0-reference",
                         "locationmap-elev-cst-ln-s0-reference",
                         "locationmap-admn-ad0-ln-s0-surroundingcountries",
                         "locationmap-admn-ad0-py-s0-scaling",
                         "locationmap-admn-ad0-py-s0-surroundingcountries"]},
                {'code':["MA8006"],
                 'maps':["atlas-admin1-boundaries-and-pcodes-plus-admin2-boundaries.mxd"],
                 'titl':["Atlas Admin 1 Boundaries and P-Codes plus Admin 2 Boundaries"],
                 'summ':["Atlas Admin 1 Boundaries and P-Codes plus Admin 2 Boundaries and PCodes"],
                 'temp':["reference"],
                 'main':["mainmap-admn-ad0-py-s0-scaling",
                         "mainmap-stle-stl-pt-s0-allmaps",
                         "mainmap-elev-cst-ln-s0-allmaps",
                         "mainmap-admn-ad0-ln-s0-reference",
                         "mainmap-admn-ad1-ln-s0-reference",
                         "mainmap-admn-ad2-ln-s1-reference",
                         "mainmap-admn-ad0-ln-s0-surroundingcountries",
                         "mainmap-admn-ad1-py-s0-reference",
                         "mainmap-admn-ad2-py-s1-reference",
                         "mainmap-carto-fea-py-s0-allmaps",
                         "mainmap-admn-ad0-py-s0-surroundingcountries",
                         "mainmap-admn-ad1-py-s1-ddpadmin1",
                         "locationmap-admn-ad1-ln-s0-reference",
                         "locationmap-carto-fea-py-s0-reference",
                         "locationmap-elev-cst-ln-s0-reference",
                         "locationmap-admn-ad0-ln-s0-surroundingcountries",
                         "locationmap-admn-ad0-py-s0-scaling",
                         "locationmap-admn-ad0-py-s0-surroundingcountries"]}
               ]
    # Return the maps dictionary
    return mapsdict

################################################################################
# Returns the configuration settings for the report generation
def framconfig():

    framdict = [
                {'fram':["Main map"],
                 'data':["mainmap-admn-ad0-py-s0-scaling"]},

                {'fram':["Location map"],
                 'data':["locationmap-admn-ad0-py-s0-scaling"]}
               ]
    # Return the fram (data frame) dictionary
    return framdict

################################################################################
# Returns the configuration settings for the data
def dataconfig():

    datadict = [
                {'lyrs':["mainmap-admn-ad0-py-s0-scaling"],
                 'name':["_admn_ad0_py_*_*_pp*.shp"],
                 'iso3':[""],                        'dirs':["202_admn"],
                 'fram':["Main map"]},

                {'lyrs':["mainmap-stle-stl-pt-s0-allmaps"],
                 'name':["_stle_stl_pt_*_*_pp*.shp"],
                 'iso3':[""],                        'dirs':["229_stle"],
                 'fram':["Main map"]},

                {'lyrs':["mainmap-tran-por-pt-s0-allmaps"],
                 'name':["_tran_por_pt_*_*_pp*.shp"],
                 'iso3':[""],                        'dirs':["232_tran"],
                 'fram':["Main map"]},

                {'lyrs':["mainmap-tran-air-pt-s0-allmaps"],
                 'name':["_tran_air_pt_*_*_pp*.shp"],
                 'iso3':[""],                        'dirs':["232_tran"],
                 'fram':["Main map"]},

                {'lyrs':["mainmap-elev-cst-ln-s0-allmaps"],
                 'name':["_elev_cst_ln_*_*_pp*.shp"],
                 'iso3':[""],                        'dirs':["211_elev"],
                 'fram':["Main map"]},

                {'lyrs':["mainmap-admn-ad0-ln-s0-reference"],
                 'name':["_admn_ad0_ln_*_*_pp*.shp"],
                 'iso3':[""],                        'dirs':["202_admn"],
                 'fram':["Main map"]},

                {'lyrs':["mainmap-tran-rds-ln-s0-allmaps"],
                 'name':["_tran_rds_ln_*_*_pp*.shp"],
                 'iso3':[""],                        'dirs':["232_tran"],
                 'fram':["Main map"]},

                {'lyrs':["mainmap-tran-rrd-ln-s0-allmaps"],
                 'name':["_tran_rrd_ln_*_*_pp*.shp"],
                 'iso3':[""],                        'dirs':["232_tran"],
                 'fram':["Main map"]},

                {'lyrs':["mainmap-phys-riv-ln-s0-reference"],
                 'name':["_phys_riv_ln_*_*_pp*.shp"],
                 'iso3':[""],                        'dirs':["221_phys"],
                 'fram':["Main map"]},

                {'lyrs':["mainmap-phys-wat-py-s0-allmaps"],
                 'name':["_phys_wat_py_*_*_pp*.shp"],
                 'iso3':[""],                        'dirs':["221_phys"],
                 'fram':["Main map"]},

                {'lyrs':["mainmap-admn-ad1-ln-s0-reference"],
                 'name':["_admn_ad1_ln_*_*_pp*.shp"],
                 'iso3':[""],                        'dirs':["202_admn"],
                 'fram':["Main map"]},

                {'lyrs':["mainmap-admn-ad2-ln-s1-reference"],
                 'name':["_admn_ad2_ln_*_*_pp*.shp"],
                 'iso3':[""],                        'dirs':["202_admn"],
                 'fram':["Main map"]},

                {'lyrs':["mainmap-elev-dem-ras-s0-reference"],
                 'name':["_elev_dem_ras_*_*_pp*.tif"],
                 'iso3':[""],                        'dirs':["211_elev"],
                 'fram':["Main map"]},

                {'lyrs':["mainmap-elev-hsh-ras-s0-reference"],
                 'name':["_elev_hsh_ras_*_*_pp*.tif"],
                 'iso3':[""],                        'dirs':["211_elev"],
                 'fram':["Main map"]},

                {'lyrs':["mainmap-admn-ad1-py-s0-reference"],
                 'name':["_admn_ad1_py_*_*_pp*.shp"],
                 'iso3':[""],                        'dirs':["202_admn"],
                 'fram':["Main map"]},

                {'lyrs':["mainmap-admn-ad2-py-s1-reference"],
                 'name':["_admn_ad2_py_*_*_pp*.shp"],
                 'iso3':[""],                        'dirs':["202_admn"],
                 'fram':["Main map"]},

                {'lyrs':["mainmap-admn-ad1-py-s1-ddpadmin1"],
                 'name':["_admn_ad1_py_*_*_pp*.shp"],
                 'iso3':[""],                        'dirs':["202_admn"],
                 'fram':["Main map"]},

                {'lyrs':["mainmap-admn-ad0-ln-s0-surroundingcountries"],
                 'name':["_admn_ad0_ln_*_*_pp*.shp"],
                 'iso3':["reg"],                     'dirs':["202_admn"],
                 'fram':["Main map"]},

                {'lyrs':["mainmap-carto-fea-py-s0-allmaps"],
                 'name':["_carto_fea_py_*_*_pp*.shp"],
                 'iso3':[""],                        'dirs':["207_carto"],
                 'fram':["Main map"]},

                {'lyrs':["mainmap-admn-ad0-py-s0-surroundingcountries"],
                 'name':["_admn_ad0_py_*_*_pp*.shp"],
                 'iso3':["reg"],                     'dirs':["202_admn"],
                 'fram':["Main map"]},

                {'lyrs':["locationmap-carto-fea-py-s0-reference"],
                 'name':["_carto_fea_py_*_*_pp*.shp"],
                 'iso3':[""],                        'dirs':["207_carto"],
                 'fram':["Location map"]},

                {'lyrs':["locationmap-elev-cst-ln-s0-reference"],
                 'name':["_elev_cst_ln_*_*_pp*.shp"],
                 'iso3':[""],                        'dirs':["211_elev"],
                 'fram':["Location map"]},

                {'lyrs':["locationmap-admn-ad1-ln-s0-reference"],
                 'name':["_admn_ad1_ln_*_*_pp*.shp"],
                 'iso3':[""],                        'dirs':["202_admn"],
                 'fram':["Location map"]},

                {'lyrs':["locationmap-admn-ad0-py-s0-scaling"],
                 'name':["_admn_ad0_py_*_*_pp*.shp"],
                 'iso3':[""],                        'dirs':["202_admn"],
                 'fram':["Location map"]},

                {'lyrs':["locationmap-admn-ad0-ln-s0-surroundingcountries"],
                 'name':["_admn_ad0_ln_*_*_pp*.shp"],
                 'iso3':["reg"],                     'dirs':["202_admn"],
                 'fram':["Location map"]},

                {'lyrs':["locationmap-admn-ad0-py-s0-reference"],
                 'name':["_admn_ad0_py_*_*_pp*.shp"],
                 'iso3':[""],                        'dirs':["202_admn"],
                 'fram':["Location map"]},

                {'lyrs':["locationmap-admn-ad0-py-s0-surroundingcountries"],
                 'name':["_admn_ad0_py_*_*_pp*.shp"],
                 'iso3':["reg"],                     'dirs':["202_admn"],
                 'fram':["Location map"]}
                ]
    # Return the data dictionary
    return datadict

################################################################################
# Returns the configuration settings for the legend elements
def elemconfig():

    elemdict = [
                {'temp':["landscape_bottom"],
                 'cenx':["231.25"],             'ceny':["37.5"]},
                {'temp':["landscape_side"],
                 'cenx':["41.75"],              'ceny':["152.25"]},
                {'temp':["portrait_bottom"],
                 'cenx':["141.5"],              'ceny':["37.5"]}
               ]

    # Return the elem (map elements) dictionary
    return elemdict
