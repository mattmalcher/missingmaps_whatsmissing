from __future__ import division
from osgeo import gdal
# import json
# import math
# import png
import numpy as np
import numpy.ma as ma

def array_to_raster(array,geotransform,projection):

    dst_filename = 'djibouti_missing_maps.tiff'

    driver = gdal.GetDriverByName('GTiff')

    dataset = driver.Create(
        dst_filename,
        len(array[0]),
        len(array),
        1,
        gdal.GDT_Float32, )

    dataset.SetGeoTransform(geotransform)

    dataset.SetProjection(projection)
    dataset.GetRasterBand(1).WriteArray(array)
    dataset.FlushCache()

#Set GeoTiff driver
driver = gdal.GetDriverByName("GTiff")
driver.Register()

#Open raster and read number of rows, columns, bands
#dataset = gdal.Open('geotiff/ECU_ppp_v2b_2015_UNadj.tif')
dataset = gdal.Open('Input Data/WorldPop/162_DJI15adjv4/DJI15adjv4.tif')
cols = dataset.RasterXSize
print cols
rows = dataset.RasterYSize
print rows

# https://stackoverflow.com/questions/2922532/obtain-latitude-and-longitude-from-a-geotiff-file
# geet geotiff spec
gt = dataset.GetGeoTransform()
minx = gt[0]
miny = gt[3] + rows*gt[4] + cols*gt[5]
maxx = gt[0] + rows*gt[1] + cols*gt[2]
maxy = gt[3]

print gt

allBands = dataset.RasterCount
band = dataset.GetRasterBand(1)

a = band.GetNoDataValue()
band.SetNoDataValue(0)

b = band.GetNoDataValue()



ndv = -3.40282346639e+38

#raster image as a list of lists
rasterarray = band.ReadAsArray(0,0,cols,rows).astype(np.float)

masked_raster = ma.masked_where(rasterarray == ndv, rasterarray )

masked_raster[0][0]

print('debug')

