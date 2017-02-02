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

    var marker = new google.maps.Marker({
        position: suggest.location,
        map: gMap,
        title: 'H'
    });
}


jQuery(window).load(function () {
    var $ = jQuery;

    $(document).on('click', '[data-toggle="lightbox"]', function (event) {
        event.preventDefault();
        $(this).ekkoLightbox();
    });

    FB.Event.subscribe('edge.create', function () {
        $.post('')
    });
});
