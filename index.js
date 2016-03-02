'use strict';

var tileReduce = require('tile-reduce');
var path = require('path');
var csv = require('fast-csv');
var fs = require('fs');
var slowStream = require('slow-stream');
var tileCover = require('tile-cover');
var tilelive = require('tilelive');
require('mbtiles').registerProtocols(tilelive);

var output = [];
var inProcess = 0;

var listsrc = function(src){ console.log('src: ' + src); }
tilelive.list('tiles', listsrc);

var stream = fs.createReadStream("output.csv");
/*
var csvStream = csv()
    .on("data", function(data){
         console.log("Row: "+data[0]);
         console.log("In Process: ", inProcess);
         getBuildings([data[2],data[3],data[4],data[5]],data[0],data[1],data[6]);
    })
    .on("end", function(){
         var ws = fs.createWriteStream("nodeoutput.csv");
		 csv
		   .write(output, {headers: true})
		   .pipe(ws);
	});

stream.pipe(csvStream).pipe(new slowStream({ maxWriteInterval: 100000 }));

function getBuildings(bbox,row,col,pop){
	inProcess++;
	var geojson = { "type": "Polygon","coordinates": [[ [bbox[0],bbox[1]], [bbox[2], bbox[1]], [bbox[2],bbox[3]], [bbox[0], bbox[3]], [bbox[0],bbox[1]] ]]};
	console.log(bbox);
	console.log(tileCover.tiles(geojson,{min_zoom: 12,max_zoom: 12}));
	tilelive.load('tiles/liberia.mbtiles', function(err, source) {
		if(err){
			console.log(err);	
		} else {		
			source.getTile(z, x, y, function(err, tile, headers) {
	            if (err) {
	            	console.log(err);
	            } else {
	            	console.log(tile);
	            }
	        });
		}
    });	
}

/*
function getBuildings(bbox,row,col,pop){
	inProcess++
	bbox=[-10.768933062289726,6.346656371823055,-10.768086319256856,6.347476442214005]
	console.log(bbox);
	var numFeatures = 0;
	tileReduce({
	  //monrovia
	  //bbox: [-10.8335,6.2465,-10.6775,6.3458],
	  maxWorkers: 1,
	  bbox:bbox,
	  //bbox: [-10.84,6.25,-10.69,6.33],
	  //liberia
	  //bbox: [-12.755,3.777,-2.769,9.644],
	  //bbox: [-15,-15,15,15],
	  //geojson:{ "type": "Polygon","coordinates": [[ [-10.8335,6.2465], [-10.6775, 6.2465], [-10.6775,6.3458], [-10.8335, 6.3458], [-10.8335,6.2465] ]]},
	  //sierra 
	  //bbox:[-13.45,6.68,-10.18,10.24],
	  zoom: 12,
	  map: path.join(__dirname, '/count.js'),
	  sources: [{name: 'osmdata', mbtiles: path.join(__dirname, 'tiles/liberia.mbtiles')}]
	})
	.on('reduce', function(num) {
	  numFeatures += num;
	})
	.on('end', function() {
	  console.log("Finished Count");
	  console.log([row,col,pop,numFeatures]);
	  output.push([row,col,pop,numFeatures]);
	  inProcess--;
	});
}
*/