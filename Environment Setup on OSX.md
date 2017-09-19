# Setting up working environment
## Getting GDAL Working via Homebrew - Abandoned
The GDAL library is used for the parsing of the Geotiff information provided by the worldpop project. It can handle vector and raster data. 
http://www.gdal.org/

For tips on installing GDAL and getting it talking to python see: https://github.com/dezhin/pygdal/ 


Get homebrew QGIS & bundled GDAL set up on macOS Sierra: https://github.com/OSGeo/homebrew-osgeo4mac

## Getting GDAL working on system python
Install the GDAL Complete package from:
http://www.kyngchaos.com/software/frameworks

This will get GDAL setup and linked to OSX system python

It does not include ogr2ogr.py which is used for converting from one format to another. This can be found here:
https://gis.stackexchange.com/questions/39080/how-do-i-use-ogr2ogr-to-convert-a-gml-to-shapefile-in-python