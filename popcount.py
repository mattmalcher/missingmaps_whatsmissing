from __future__ import division
import gdal
import json
import math
import png
import numpy as np

#Set GeoTiff driver
driver = gdal.GetDriverByName("GTiff")
driver.Register()

#Open raster and read number of rows, columns, bands
#dataset = gdal.Open('geotiff/ECU_ppp_v2b_2015_UNadj.tif')
dataset = gdal.Open('geotiff/ECU_ppp_v2b_2015_UNadj.tif')
cols = dataset.RasterXSize
print cols
rows = dataset.RasterYSize
print rows

#get geotiff spec
gt = dataset.GetGeoTransform()
minx = gt[0]
miny = gt[3] + rows*gt[4] + cols*gt[5] 
maxx = gt[0] + rows*gt[1] + cols*gt[2]
maxy = gt[3]

print gt

allBands = dataset.RasterCount
band = dataset.GetRasterBand(1)

#raster image as a list of lists
rasterarray = band.ReadAsArray(0,0,cols,rows)

#create empty osm array of 0s
osmarray = [[0 for i in range(cols)] for j in range(rows)]
print "Loading geojson:"

with open('ecuador_buildings.geojson') as data_file:
    data = json.load(data_file)
    countf = len(data['features'])
    i=0
    print "Number of features:"
    print countf
    #loop through each building and increase count on relevant osmarray value
    for f in data['features']:
        
        i+=1
        if i%2500==0:
            print i/countf
        #different number of nested lists to get coordinates for different geojson
        #print feature to see how many are need. Improve script in future
        #print f
        col = int(math.floor((f['geometry']['coordinates'][0][0][0][0]-gt[0])/gt[1]))
        row = int(math.floor((f['geometry']['coordinates'][0][0][0][1]-gt[3])/gt[5]))
        if col>cols:
            print "col"
            print col
        if row>rows:
            print "row"
            print row
        osmarray[row][col] = osmarray[row][col] +1


print "Counting pop"

totalpop = 0

for row in range(0,rows):
    for col in range(0,cols):
        buildings = 0
        for x in range(-5,6):
            for y in range(-5,6):
                if col+x>-1 and col+x<cols and row+y>-1 and row+y < rows:
                    buildings = osmarray[row+y][col+x]
        if buildings == 0 and rasterarray[row][col]>0:
            totalpop = totalpop + rasterarray[row][col]
            print totalpop
        



