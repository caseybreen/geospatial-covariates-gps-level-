"""
Created on Thu Jan 26 09:28:56 2017

@author: cbreen

This script performs extract values to points for a set of focal statistics rasters
"""

# Import 
import os
import sys
import string
import arcpy,csv
from arcpy.sa import *
arcpy.CheckOutExtension("spatial")
arcpy.CheckOutExtension("GeoStats")

#Import date and time 
import datetime  
start = datetime.datetime.now()  
print 'start run: %s\n' % (start) 

# path to input focal statistic rasters
fs_rasters = "C:/workspace/chirps/processing/fs_rasters/"
out_extract = "C:/workspace/chirps/processing/gps_extract/"
dataGDB ="C:/workspace/chirps/processing/data.gdb/"

# Path to GPS points
gpsPoints = "C:/workspace/chirps/gps/"

arcpy.env.workspace = fs_rasters
tiffs = arcpy.ListRasters("*")


i = 1 
for tiff in tiffs:
    tiffSplit = tiff.split("_")
    year = tiffSplit[1]
    month = tiffSplit[2]
     
#Extract Values to Points   *** Change GPS point here*** 
    arcpy.gp.ExtractValuesToPoints_sa(gpsPoints + "GPS_final.shp", fs_rasters + "fc_" + year + "_" + month, out_extract + "out_" + year + "_" + month+ ".shp", "NONE", "VALUE_ONLY")
    print 'finished values to Table run: %s\n\n' % (datetime.datetime.now() - start)

#Copy extract by points table to Geodatabase 
    arcpy.TableToGeodatabase_conversion(Input_Table=out_extract + "out_" + year + "_" + month, Output_Geodatabase='C:/workspace/chirps/processing/data.gdb/')
    century_year = (int(year)-1900)*12+int(month)
    arcpy.AddField_management(dataGDB + "out_" + year + "_" + month,"CenturyMonth","FLOAT","","","7","","NULLABLE","NON_REQUIRED","")
    arcpy.CalculateField_management(in_table=dataGDB + "out_" + year + "_" + month, field="CenturyMonth", expression= century_year, expression_type="VB", code_block="")

#Table to CSV
    arcpy.TableToTable_conversion(dataGDB + "out_" + year + "_" + month, out_csv, "csv" + year + "_" + month + ".csv")
    print i
    print 'finished with month run: %s\n\n' % (datetime.datetime.now() - start)
    i=i+1
    
print 'finished all run: %s\n\n' % (datetime.datetime.now() - start)



