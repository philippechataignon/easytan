<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="utf-8">
    <title>EasyTan | Carte</title>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
    <style type="text/css">
        html { height: 100% }
        body { height: 100%; margin: 0; padding: 0 }
    </style>

    <script src="/static/js/jquery.min.js"></script>
    <script type="text/javascript"
      src="http://maps.googleapis.com/maps/api/js?key=AIzaSyCZIX_wp4bM27biaMpSEFiTinVpGh174t0&sensor=false">
    </script>
    <script type="text/javascript">
    var map;
    var markers = [];
    function mapInit(){
        var mapOptions = {
            zoom: ${zoom},
            center: new google.maps.LatLng(${center.stop_lat}, ${center.stop_lon}),
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        map = new google.maps.Map(document.getElementById("map"), mapOptions);

    }

    function getMarkers(bounds) {
        var southWest = bounds.getSouthWest();
        var northEast = bounds.getNorthEast();
        $.getJSON("/json_map",
            {
                zoom: map.getZoom(),
                latl: southWest.lat(),
                lath: northEast.lat(),
                lonl: southWest.lng(),
                lonh: northEast.lng()
            },
            function(data){
            $.each(data, function(key, item){
                var marker = new google.maps.Marker({
                    position: new google.maps.LatLng(item.lat, item.lon),
                    map: map,
                    title: item.id + ' - ' + item.nom,
                    id: item.id,
                    loc_type: item.loc_type
                });
                if (marker.loc_type == 1) {
                    marker.icon = '/static/images/busstop.png';
                }
                markers.push(marker);
                google.maps.event.addListener(marker, 'click', function() {
                    if (map.getZoom() >= 16) {
                        window.location.href = "/stop/" + this.id ;
                    } else {
                        window.location.href = "/map/" + this.id ;
                    }
                });
            });
        });
    }

    $(function(){
        mapInit();
        google.maps.event.addListenerOnce(map, 'bounds_changed', function() {
            var bounds = map.getBounds();
            getMarkers(bounds);
        });
        google.maps.event.addListener(map, 'idle', function() {
            var bounds = map.getBounds();
            getMarkers(bounds);
        });
    });
    </script>
</head>

<body>
    <div id="map" style="width:100%; height:100%"></div>
</body>
</html>
