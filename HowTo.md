#Introduction
Aim of this project is to work the 'Where are the Maps Missing' scripts made by Simon Johnson into a tool.

##What is 'Where are the Maps Missing'?
Where are the maps missing is work associated with the missing maps project http://www.missingmaps.org. It was used to produce the maps found in the blog post at: https://medium.com/@Simon_B_Johnson/where-are-the-maps-missing-b22ceedb26f3



# Data

## World Population Geotiffs
The index of world population are taken from: http://www.worldpop.org.uk/data

## OSM Building Density
Overpass queries for all buildings in a country or ISO_3166-1 region tend to fail unless the country is very small.

Alternative is to use the country osm files from: http://download.geofabrik.de
Unclear how this could be automated though.

It is then neccesary to convert the OSM file to GeoJson:
https://gist.github.com/tecoholic/1396990

alternatively, potential to use gdal for this: https://gis.stackexchange.com/questions/22788/how-do-you-convert-osm-xml-to-geojson/69622#69622


(with the current script, maybe we could parse the OSM xml in the script?)