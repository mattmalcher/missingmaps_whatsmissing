from __future__ import division
import gdal
import json
import math
import png
import numpy as np

def array_to_raster(array,geotransform,projection):

    dst_filename = 'ecuador_missing_maps.tiff'

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
dataset = gdal.Open('geotiff/ECU_ppp_v2b_2015_UNadj.tif')
cols = dataset.RasterXSize
print cols
rows = dataset.RasterYSize
print rows

#geet geotiff spec
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
#with open('ecuador_buildings.geojson') as data_file:
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


######This section can be skipped for speed.  Produces osm png and worldpop png

#find max building count to normalise against
##        
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

########end of part you can skip

print "Creating difference array"

differencearray = [[0 for i in range(cols)] for j in range(rows)]

for row in range(0,rows):
    for col in range(0,cols):
        buildings = osmarray[row][col]
        if buildings == 0:
            #minimum building value
            buildings = 0.01
        
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

#pngarray = [[255 for i in range(cols)] for j in range(rows)]
pngarray = np.zeros((rows, cols))
for row in range(0,rows):
    for col in range(0,cols):
        #if differencearray[row][col]>0:
            #value = int(math.floor(math.log(differencearray[row][col])/math.log(maxdifference)*maxdifference))
            value = int(math.floor(differencearray[row][col]))
            pngarray[row][col] = value

projection = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.01745329251994328,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]]'
array_to_raster(pngarray,gt,projection)
#with open('liberia_difference_0.1_cutoff_1_no_log.png', 'wb') as png_file:
#    print len(pngarray[0])
#    print len(pngarray)
#    w = png.Writer(len(pngarray[0]), len(pngarray), greyscale=True, bitdepth=8)
#    w.write(png_file, pngarray);
