'use strict';

var tileReduce = require('tile-reduce');
var path = require('path');

var numFeatures = 0;

tileReduce({
  //monrovia
  //bbox: [-10.8335,6.2465,-10.6775,6.3458],
  bbox: [-10.84,6.25,-10.69,6.33],
  //liberia
  //bbox: [-12.755,3.777,-2.769,9.644],
  //bbox: [-15,-15,15,15],
  //geojson:{ "type": "Polygon","coordinates": [[ [-10.8335,6.2465], [-10.6775, 6.2465], [-10.6775,6.3458], [-10.8335, 6.3458], [-10.8335,6.2465] ]]},
  zoom: 15,
  map: path.join(__dirname, '/count.js'),
  sources: [{name: 'osm', mbtiles: path.join(__dirname, 'tiles/liberia.mbtiles')}]
})
.on('reduce', function(num) {
  numFeatures += num;
})
.on('end', function() {
  console.log('Features total: %d', numFeatures);
});
