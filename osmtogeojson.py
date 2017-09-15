# https://gis.stackexchange.com/questions/22788/how-do-you-convert-osm-xml-to-geojson/69622#69622
# https://gis.stackexchange.com/questions/39080/using-ogr2ogr-to-convert-gml-to-shapefile-in-python
# http://svn.osgeo.org/gdal/trunk/gdal/swig/python/samples/ogr2ogr.py

from osgeo import ogr2ogr # Note - this does not exist by default - copy python port from above url

def main():
  #note: main is expecting sys.argv, where the first argument is the script name
  #so, the argument indices in the array need to be offset by 1
  ogr2ogr.main(["","-f", "GeoJSON", "out.geojson", "Input Data/OSM/bangladesh-latest.osm","multipolygons"])

main()