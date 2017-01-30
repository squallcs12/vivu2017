/**
 * Created by bang on 24/01/2017.
 */
var gMap;

function initMap() {
    // Create a map object and specify the DOM element for display.
    gMap = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 16.60, lng: 105.65},
        zoom: 6
    });

    function markerClick(place, event) {
        gMap.setCenter({
            lat: event.latLng.lat(),
            lng: event.latLng.lng()
        });

        if (gMap.getZoom() < 13) {
            gMap.setZoom(13);
        } else {
            location.href = place.href;
        }
    }

    for (var i = 0; i < chosenPlaces.length; i++) {
        var place = chosenPlaces[i];
        var marker = new google.maps.Marker({
            position: place.location,
            map: gMap,
            title: place.name
        });

        google.maps.event.addListener(marker, 'click', markerClick.bind(marker, place))
    }
}
