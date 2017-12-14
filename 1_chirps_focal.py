# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 09:28:56 2017

@author: cbreen

This script calculates Focal Statistics Rasters
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


##paths to input data
rasters ="C:/workspace/chirps/rasters/"
gpsPoints = "C:/workspace/chirps/gps/"

##paths to processing data
clip_rasters_1 = "C:/workspace/chirps/processing/clip_1/"
resample_raster ="C:/workspace/chirps/processing/resample_raster/"
clip_rasters_2 = "C:/workspace/chirps/processing/clip_2/"
fs_rasters = "C:/workspace/chirps/processing/fs_rasters/"

##path to output data
out_extract = "C:/workspace/chirps/processing/gps_extract/"
dataGDB ="C:/workspace/chirps/processing/data.gdb/"
out_csv = "C:/workspace/chirps/csv/"
#focal_extract = "C:/Workspace/gates/gps/focal_extract/merge_157.shp"

arcpy.env.workspace = rasters
tiffs = arcpy.ListRasters("*")

#Resample all Raster 
i = 1 
for tiff in tiffs:
     tiffSplit = tiff.split(".")
     year=tiffSplit[2]
     month=tiffSplit[3]
# Clip Raster 
     arcpy.Clip_management(in_raster=rasters+ tiff, rectangle="-92.9054565429688 -42.5033569335938 129.547058105469 50.6832275390625", out_raster=clip_rasters_1 + tiff, in_template_dataset="C:/Workspace/gates/gps/clips/clip_5.shp", nodata_value="-3.402823e+038", clipping_geometry="ClippingGeometry", maintain_clipping_extent="NO_MAINTAIN_EXTENT")     
     print 'finished clip1.0 run: %s\n\n' % (datetime.datetime.now() - start)
#Resample Raster
     arcpy.Resample_management(clip_rasters_1 + tiff , resample_raster + "re_" + year + "_" + month, cell_size="5.00000007450581E-03 5.00000007450581E-03", resampling_type="NEAREST")
     print 'finished resample run: %s\n\n' % (datetime.datetime.now() - start)
# Clip Resampled Rasters
     arcpy.Clip_management(in_raster= resample_raster + "re_" + year + "_" + month, rectangle="-93.571600 -33.266541 129.532900 51.962759", out_raster=clip_rasters_2 + "re_" + year + "_" + month, in_template_dataset="C:/Workspace/gates/gps/clips/water_clip.shp", nodata_value="-3.402823e+038", clipping_geometry="ClippingGeometry", maintain_clipping_extent="NO_MAINTAIN_EXTENT")
     print 'finished with clip2.0 run: %s\n\n' % (datetime.datetime.now() - start)

#Run Focal Statistics
     arcpy.env.workspace = clip_rasters_2
     outFocalStatistics = FocalStatistics("re_" + year + "_" + month, "Circle 4 CELL", "MEAN", "Data")
     outFocalStatistics.save(fs_rasters + "fc_" + year + "_" + month)
     print 'finished resample and focal run: %s\n\n' % (datetime.datetime.now() - start)

#Delete Raster
     arcpy.Delete_management(in_data= clip_rasters_1 + tiff, data_type  = "Raster Dataset")
     arcpy.Delete_management(in_data= resample_raster + "re_" + year + "_" + month, data_type  = "Raster Dataset")
     arcpy.Delete_management(in_data= clip_rasters_2 + "re_" + year + "_" + month, data_type  = "Raster Dataset")

     print i
     print 'finished with month run: %s\n\n' % (datetime.datetime.now() - start)
     i=i+1     
print 'finished all run: %s\n\n' % (datetime.datetime.now() - start)


     
