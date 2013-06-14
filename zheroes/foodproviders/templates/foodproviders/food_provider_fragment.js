var x = function() {
    var infowindow = new google.maps.InfoWindow({
        content: "{{ fp.description_as_html | escapejs }}"
    });
    var marker = new google.maps.Marker({
        position: new google.maps.LatLng({{ fp.location.x }}, {{ fp.location.y }}),
        map: map,
        title: "{{ fp.name | escapejs }}"
    });
    console.log(marker)
    google.maps.event.addListener(marker, 'click', function() {
      infowindow.open(map,marker);
    });
}
x()
