from __future__ import division
import gdal
import json
import math
import png

#Set GeoTiff driver
driver = gdal.GetDriverByName("GTiff")
driver.Register()

#Open raster and read number of rows, columns, bands
#dataset = gdal.Open('geotiff/ECU_ppp_v2b_2015_UNadj.tif')
dataset = gdal.Open('geotiff/LBR10adjv3.tif')
cols = dataset.RasterXSize
print cols
rows = dataset.RasterYSize
print rows


gt = dataset.GetGeoTransform()
minx = gt[0]
miny = gt[3] + rows*gt[4] + cols*gt[5] 
maxx = gt[0] + rows*gt[1] + cols*gt[2]
maxy = gt[3]

print gt

allBands = dataset.RasterCount
band = dataset.GetRasterBand(1)

rasterarray = band.ReadAsArray(0,0,cols,rows)

osmarray = [[0 for i in range(cols)] for j in range(rows)]
print "Loading geojson:"
#with open('ecuador_buildings.geojson') as data_file:
with open('liberia_buildings.geojson') as data_file:
    data = json.load(data_file)
    countf = len(data['features'])
    i=0
    print "Number of features:"
    print countf
    for f in data['features']:
        
        i+=1
        if i%2500==0:
            print i/countf
        #different number of nested lists to get coordinates for different geojson
        #print feature to see how many are need. Improve script in future
        #print f
        col = int(math.floor((f['geometry']['coordinates'][0][0][0]-gt[0])/gt[1]))
        row = int(math.floor((f['geometry']['coordinates'][0][0][1]-gt[3])/gt[5]))
        if col>cols:
            print "col"
            print col
        if row>rows:
            print "row"
            print row
        osmarray[row][col] = osmarray[row][col] +1
    
##maxBuildings = 0
##
##print "Finding Max building count"
##for row in osmarray:
##    for cell in row:
##        if cell>maxBuildings:
##            maxBuildings = cell
##
##print maxBuildings
##
##print "Creating osm png"
##pngarray = [[255 for i in range(cols)] for j in range(rows)]
##for row in range(0,rows):
##    for col in range(0,cols):
##        if osmarray[row][col]>0:
##            pngarray[row][col] = 255-int(math.floor(math.log(osmarray[row][col])/math.log(maxBuildings)*255))
##
##with open('ecuador_osm.png', 'wb') as png_file:
##    print len(pngarray[0])
##    print len(pngarray)
##    w = png.Writer(len(pngarray[0]), len(pngarray), greyscale=True, bitdepth=8)
##    w.write(png_file, pngarray)
##                                            
##maxPop = 0
##
##print "Finding Max building count"
##for row in rasterarray:
##    for cell in row:
##        if cell>maxPop:
##            maxPop = cell
##
##print maxPop
## 
##print "Creating world pop png"
##
##pngarray = [[255 for i in range(cols)] for j in range(rows)]
##for row in range(0,rows):
##    for col in range(0,cols):
##        if rasterarray[row][col]>1:
##            value = 255-int(math.floor(math.log(rasterarray[row][col])/math.log(maxPop)*255))
##            pngarray[row][col] = value
##
##with open('ecuador_worldpop.png', 'wb') as png_file:
##    print len(pngarray[0])
##    print len(pngarray)
##    w = png.Writer(len(pngarray[0]), len(pngarray), greyscale=True, bitdepth=8)
##    w.write(png_file, pngarray);

print "Creating difference array"

differencearray = [[0 for i in range(cols)] for j in range(rows)]

for row in range(0,rows):
    for col in range(0,cols):
        buildings = osmarray[row][col]
        if buildings == 0:
            buildings = 0.1
        
        value = rasterarray[row][col]/buildings+1
        differencearray[row][col] = value



print "Finding Max difference"

maxdifference = 0

for row in differencearray:
    for cell in row:
        if cell>maxdifference:
            maxdifference = cell

print maxdifference
 
print "Creating difference png"

pngarray = [[255 for i in range(cols)] for j in range(rows)]
for row in range(0,rows):
    for col in range(0,cols):
        if differencearray[row][col]>1:
            value = 255-int(math.floor(math.log(differencearray[row][col])/math.log(maxdifference)*255))
            pngarray[row][col] = value

with open('liberia_difference_0.1_cutoff_1_no_log.png', 'wb') as png_file:
    print len(pngarray[0])
    print len(pngarray)
    w = png.Writer(len(pngarray[0]), len(pngarray), greyscale=True, bitdepth=8)
    w.write(png_file, pngarray);
