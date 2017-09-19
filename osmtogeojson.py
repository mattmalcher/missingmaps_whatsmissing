# https://gis.stackexchange.com/questions/22788/how-do-you-convert-osm-xml-to-geojson/69622#69622
# https://gis.stackexchange.com/questions/39080/using-ogr2ogr-to-convert-gml-to-shapefile-in-python
# http://svn.osgeo.org/gdal/trunk/gdal/swig/python/samples/ogr2ogr.py
import os

from osgeo import ogr2ogr # Note - this does not exist by default - copy python port from above url

def convert(filename, indir ,outdir):
  #note: main is expecting sys.argv, where the first argument is the script name
  #so, the argument indices in the array need to be offset by 1
  ogr2ogr.main(["","-f", "GeoJSON",
                os.path.join(outdir, filename)+".geojson",
                os.path.join(indir, filename),
                "multipolygons"])


indir="Input Data/OSM"

outdir="Input Data/Converted"

# Get list of files in InputData/OSM

# Check for equivalent file in converted

# Generate geojson

for filename in os.listdir(indir):

    if filename.endswith(".osm") or filename.endswith(".osm.pbf"):

      if os.path.isfile(os.path.join(outdir, filename)+".geojson"):

        print(os.path.join(outdir, filename) + ' already exists')
        continue

      else:
        print("Converting "+filename)
        convert(filename, indir, outdir)


# Note that this geojson contains all of the multipolygon features, only some of which are buildings.
        # You can filter the buildings using layer filters in QGIS "building" IS NOT NULL
        # Need a programmatic way of doing this.
        # Feel like using some databases instead of json files might be better? Quicker to render in QGIS too.
        # PostGIS perhaps? Could use this to filter too.