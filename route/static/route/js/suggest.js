/**
 * Created by bang on 24/01/2017.
 */

(function ($) {
    var listener = 0,
        marker,
        currentPlace,
        $formattedAddress = $(".formatted_address"),
        $btnSuggest = $("#btn_suggest");

    function is_specific_address(result) {
        return result.address_components.length >= 4;
    }

    function filter_result(response) {
        for (var i = 0; i < response.results.length; i++) {
            if (is_specific_address(response.results[i])) {
                return response.results[i];
            }
        }
        return response.results[0];
    }

    function _try_display(address) {
        $.get('https://maps.googleapis.com/maps/api/geocode/json', {
            'address': address,
            'key': 'AIzaSyAwPtuLHn3q5YdVlbQ3L8Z7Z20vObX9Ws8'
        }, function (response) {
            var result = filter_result(response);


            $formattedAddress.text(result.formatted_address);

            if (!is_specific_address(result)) {
                $formattedAddress.text(
                    result.formatted_address + ". Địa chỉ này quá chung chung, nhập địa chỉ cụ thể hơn nhé");
                $btnSuggest.hide();
                return;
            }

            $btnSuggest.show();

            var location = result.geometry.location;
            gMap.setCenter(location);
            gMap.setZoom(14);

            if (marker) {
                marker.setMap(null);
            }

            marker = new google.maps.Marker({
                position: location,
                map: gMap,
                title: result.formatted_address
            });

            currentPlace = result;
        });
    }

    function try_display(address) {
        if (listener) {
            clearTimeout(listener);
        }

        listener = setTimeout(function () {
            _try_display(address);
        }, 500);
    }

    function getProvince(place) {
        for (var i = place.address_components.length -1 ; i >= 0; i--) {
            var component = place.address_components[i];
            if (component.types.indexOf('administrative_area_level_1') != -1) {
                return component.short_name;
            }
        }
        return place.address_components[place.address_components.length - 2].short_name;
    }

    function getCsrfToken() {
        return $("input[name='csrfmiddlewaretoken']").val();
    }

    function show_suggest(place) {
        $("#suggest_modal").modal('show');
    }

    function suggest(place){
        var place_info = {
            address: place.formatted_address,
            lat: place.geometry.location.lat.toFixed(2),
            lng: place.geometry.location.lng.toFixed(2),
            place_id: place.place_id,
            province: getProvince(place),
            description: $("#id_description").val()
        };

        $.ajax({
            url: '',
            type: 'post',
            data: JSON.stringify(place_info),
            headers: {
                'Content-type': 'application/json',
                'x-csrftoken': getCsrfToken()
            },
            success: function (response) {
                location.href = response.url;
            },
            fail: function () {
                console.log("Error")
            }
        });
    }

    $("#id_address").keyup(function () {
        try_display($(this).val());
    });

    $("#btn_suggest").click(function (e) {
        show_suggest(currentPlace);
    });

    $("#id_submit_suggest").click(function () {
        suggest(currentPlace);
    });
})(jQuery);
