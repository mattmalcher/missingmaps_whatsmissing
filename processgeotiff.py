import gdal
import csv

#Set GeoTiff driver
driver = gdal.GetDriverByName("GTiff")
driver.Register()

#Open raster and read number of rows, columns, bands
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

allBands = dataset.RasterCount
band = dataset.GetRasterBand(1)

rasterarray = band.ReadAsArray(0,0,cols,rows)

print "processing raster"

output = []
for row in range(0,rows):
    for col in range(0,cols):
        if(rasterarray[row][col]>0):
            bbox = [minx+(maxx-minx)*(float(col)/cols),maxy-(maxy-miny)*(float(row)/rows),minx+(maxx-minx)*(float(col+1)/cols),maxy-(maxy-miny)*(float(row+1)/rows)]
            out = [row,col,bbox[0],bbox[1],bbox[2],bbox[3],rasterarray[row][col]]
            output.append(out)
    print row

print "Writing output"
with open("output.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(output)

