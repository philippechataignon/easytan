<%inherit file="/base.mako"/>\
<%def name="title()">Accueil</%def>
<%block name="javascript">
    <script src="/static/bootstrap/js/bootstrap.js"></script>
    <script type="text/javascript">
    $(function() {
        function get_hor_api(stop_id) {
            $.getJSON(
                '/json_api', 
                {'stop_id': stop_id}, 
                function(data) {
                    var table=['<table class="table table-striped"><tr>'];
                    $.each(data.head, function(key, item){
                        table.push('<th>'+item+'</th>');
                    });
                    table.push('</tr>');
                    $.each(data.data, function(key, item){
                        table.push('<tr>');
                        table.push('<td>'+item.attente+'</td>');
                        table.push('<td><img width="25" height="25" src="/static/images/lignes/'+item.ligne+'.gif"></td>');
                        table.push('<td><img width="10" height="10" src="/static/images/'+item.sens+'.gif"></td>');
                        table.push('<td>'+item.terminus+'</td>');
                        table.push('<td>'+item.stop+'</td>');
                        table.push('</tr>');
                    });
                    table.push('</table>');
                $('#table_hor').html(table.join(''));  
                }
            );
        }
        $('#nom_station').typeahead({
            minLength: 2,
            source: function (query, process) {
                $.getJSON('/json_stops', 
                    {query: query}, 
                    function (data) {return process(data);}
                );
            }
        });
        $('#sub_map').click(function() {
            if ($('#nom_station').val().length > 0) {
                window.location.href = "/map/" + $('#nom_station').val().substr(0, 4);
            } else {
                window.location.href = "/map" ;
            }
        })
        $('#sub_api').click(function() {
            if ($('#nom_station').val().length >= 4) {
                get_hor_api($('#nom_station').val().substr(0, 5));
            }
        })
        $('#sub_hor').click(function() {
            if ($('#nom_station').val().length >= 4) {
                window.location.href = "/form/" + $('#nom_station').val().substr(0, 5);
            }
        })
    });
    </script>
</%block>

<div class="container">
    <h1>Bienvenue sur EasyTan</h1>
    <p>Cette version du site utilise la base des horaires à partir du 26 août 2013</p>
    <p>Entrer le <b>nom de votre station</b>.</p>
    <%
    stop_id = "%s - %s" % (stop.stop_id, stop.stop_name) if stop else ""
    %>
    <div class="well form-inline">
        <input type="text" id="nom_station" name="stop_id" data-provide="typeahead" autocomplete="off" value="${stop_id}"/>
        <button id="sub_map" class="btn" ><i class="icon-eye-open"></i> Voir sur une carte</button>
        <button id="sub_hor" class="btn"><i class="icon-calendar"></i> Recherche horaires</button>
        <button id="sub_api" class="btn"><i class="icon-time"></i> Horaires temps réel</button>
    </div>
    <div id="table_hor">
    </div>
</div>
