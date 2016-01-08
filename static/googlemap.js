
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
  
function initMap() {

  // Specify features and elements to define styles.
  //Getting list of JSON objects from field and parsing it.
  points = eval(document.getElementById("poi_list").innerHTML);
  //document.getElementById("test").innerHTML = typeof(points[0].lat);
  
  var map = new google.maps.Map(document.getElementById('map'), {
	styles: styleArray
  });

  setMarkers(map);
  map.fitBounds(bounds);
  map.panToBounds(bounds);
}

// Data for the markers consisting of a name, a LatLng and a zIndex for the
// order in which these markers should display on top of each other.


function setMarkers(map) {
  // Adds markers to the map.

  // Marker sizes are expressed as a Size of X,Y where the origin of the image
  // (0,0) is located in the top left of the image.

  // Origins, anchor positions and coordinates of the marker increase in the X
  // direction to the right and in the Y direction down.
  var image = {
    url: 'images/beachflag.png',
    // This marker is 20 pixels wide by 32 pixels high.
    size: new google.maps.Size(20, 32),
    // The origin for this image is (0, 0).
    origin: new google.maps.Point(0, 0),
    // The anchor for this image is the base of the flagpole at (0, 32).
    anchor: new google.maps.Point(0, 32)
  };
  // Shapes define the clickable region of the icon. The type defines an HTML
  // <area> element 'poly' which traces out a polygon as a series of X,Y points.
  // The final coordinate closes the poly by connecting to the first coordinate.
  var shape = {
    coords: [1, 1, 1, 20, 18, 20, 18, 1],
    type: 'poly'
  };

  for (var i = 0; i < points.length; i++) {
    var point = points[i];
    var marker = new google.maps.Marker({
      position: {lat: parseFloat(point.lat), lng: parseFloat(point.lng)},
      map: map,
      //icon: image,
      //shape: shape,
      title: String(point.poi_name),
      //zIndex: String(point.type)
    });
  }
  for (var p of points){
  loc = new google.maps.LatLng(parseFloat(p.lat),parseFloat(p.lng));
  bounds.extend(loc);
  }
}

google.maps.event.addDomListener(window, 'load', initMap);
