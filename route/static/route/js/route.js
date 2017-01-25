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
}
