var tileReduce = require('tile-reduce');
var path = require('path');
var fs = require('fs');
var readline = require('readline');
var stream = require('stream');

var instream = fs.createReadStream('output.csv');
var inProcess = 0;
var paused = false;
var outstream = new stream;
var rl = readline.createInterface(instream,outstream);
var output = [];
rl.on('line', function(line) {
    inProcess++;
    if(inProcess > 10) {
        console.log('pausing input to clear queue');
        rl.pause();
        paused = true;
    }
    var data = line.split(',');
    getBuildings([data[2],data[3],data[4],data[5]],data[0],data[1],data[6])
});

rl.on('end', function() {
    rl.close();
});

function getBuildings(bbox,row,col,pop){
    console.log('getting buildings');
    console.log(inProcess);
    var numFeatures = 0;
    tileReduce({
      //monrovia
      bbox: [-10.8335,6.2465,-10.6775,6.3458],
      maxWorkers: 1,
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
      output.append([row,col,pop,numFeatures]);
        inProcess--;
        if(paused && inProcess < 5) {
                console.log('resuming stream');
                paused = false;
                rl.resume();
        }

        if (err) throw err; 

    });

}