
var styleArray = [
	{
		featureType: "all",
		stylers: [
			{ saturation: -80 }
		]
    },{
		featureType: "road.arterial",
		elementType: "geometry",
		stylers: [
			{ hue: "#00ffee" },
			{ saturation: 50 }
		]
    },{
		featureType: "poi.business",
		elementType: "labels",
		stylers: [
			{ visibility: "off" }
		]
    }
];
  
var loc;  
var points;
var bounds = new google.maps.LatLngBounds();
var markers = [];
var initialPosition = {lat: 60.0, lng: 60.0};

// Set initial postion first
function getBrowserPosition(){	    
	if (navigator.geolocation) {
	// Try Browser Geolocation
		navigator.geolocation.getCurrentPosition(assignPosition);
	} else {window.alert('Browser does not support geolocation');}
}

function assignPosition(position){
	initialPosition = {
		lat: position.coords.latitude,
		lng: position.coords.longitude
	};
}

getBrowserPosition();

// initialize the map
var map = new google.maps.Map(document.getElementById('map'), {
	styles: styleArray,
	center: {
		lat: initialPosition.lat,
		lng: initialPosition.lng,
	},
	zoom: 8	
});

// set markers, center, zoom
function setMapView(point_list) {
	points = eval(point_list);
	
	if ((typeof(points) != 'object') || (points === null) || (points.length == 0)){	
		map.setCenter(initialPosition);
	}
	else{		
		setMarkers(map);
		map.fitBounds(bounds);
		map.panToBounds(bounds);
	}
}

// helpers...
function handleLocationError(browserHasGeolocation, infoWindow, pos) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(browserHasGeolocation ?
                        'Error: The Geolocation service failed.' :
                        'Error: Your browser doesn\'t support geolocation.');
}
// Data for the markers consisting of a name, a LatLng and a zIndex for the
// order in which these markers should display on top of each other.

function setMarkers(map) {
  // Adds markers to the map.
	bounds = new google.maps.LatLngBounds();
	for (var i = 0; i < points.length; i++) {
		var point = points[i];
		var marker = new google.maps.Marker({
			position: {lat: parseFloat(point.lat), lng: parseFloat(point.lng)},
			map: map,
			//icon: image,
			//shape: shape,
			title: String(point.name)
			//zIndex: String(point.type)
		});		
		bounds.extend(new google.maps.LatLng(parseFloat(point.lat),parseFloat(point.lng)));
	}		
}

$( window ).load(function() {
	setMapView(eval([]));
});