/**
 * Created by bang on 24/01/2017.
 */

var gMap;

function initMap() {
    // Create a map object and specify the DOM element for display.
    gMap = new google.maps.Map(document.getElementById('map'), {
        center: suggest.location,
        zoom: 14,
        draggable: false,
        scrollwheel: false,
        disableDoubleClickZoom: true
    });

    marker = new google.maps.Marker({
        position: suggest.location,
        map: gMap,
        title: 'H'
    });
}
