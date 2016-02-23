'use strict';

module.exports = function(data, tile, writeData, done) {
  var count = 0;
  var osmdata = data.osm.osm;
  // Count features containing the "building" key
  osmdata.features.forEach(function(feature) {
    if (feature.properties.building) {
      count++;
    }
  });
  done(null, count);
};
