var baseOSM = L.tileLayer(
        'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
        attribution: '&copy; OpenStreetMap contributors'}
);

var BING_KEY = 'AuhiCJHlGzhg93IqUH_oCpl_-ZUrIE6SPftlyGYUvr9Amx5nzA-WqGcPquyFZl4L'
var bingLayer = L.tileLayer.bing(BING_KEY);

var map = L.map('map', {
    center: [1.8312, -78.1834],
    zoom: 6,
    layers: [bingLayer]
});

var missingMap = L.tileLayer.wms("http://52.90.193.38/geoserver/ows", {
    layers: 'geonode:ecuador_missing_maps',
    format: 'image/png',
    transparent: true,
    attribution: "BRC Maps Team",
    styles:'liberia_missing_maps',
}).addTo(map);

var baseMaps = {
    "OpenStreetMap": baseOSM,
    "Bing Satellite": bingLayer
};

var overlayMaps = {
    "Missing Maps": missingMap
};

L.control.layers(baseMaps, overlayMaps).addTo(map);

var colors = ['#FC8D59','#7f0000'];
var labels = ['Low Populated area missing map','High Populated area missing map'];

var legend = L.control({position: 'bottomright'});

legend.onAdd = function (map) {

        var div = L.DomUtil.create('div', 'info legend');
                
        div.innerHTML = "<p>Map highligting unmapped areas</p>";
        for (var i = 0; i < labels.length; i++) {
            div.innerHTML +='<i style="background:' + colors[i] + '"></i> ' + labels[i] + '<br />';
        }

        return div;
    };

legend.addTo(map);

function resize(){
    $('#map').height($(window).height()-$('#header').height()-10);
    map.invalidateSize(false);
}

$(window).load(function(){
    resize();
});
$(window).resize(function(){
    resize();
});
