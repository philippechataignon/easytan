<%inherit file="/base.mako"/>\
<%def name="title()">Accueil</%def>
<%block name="javascript">
    <script src="/static/bootstrap/js/bootstrap.js"></script>
    <script type="text/javascript">
    $(function() {
        $('#nom_station').typeahead({
            minLength: 2,
            source: function (query, process) {
                $.getJSON('/json_stops', 
                    {query: query}, 
                    function (data) {
                        var resultList = data.map(function (item) {
                            return item.id + ' - ' + item.name + ' (' + item.commune + ')';
                        });
                        return process(resultList);
                    }
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
        $('#sub_hor').click(function() {
            if ($('#nom_station').val().length >= 4) {
                window.location.href = "/form/" + $('#nom_station').val().substr(0, 4);
            }
        })
    });
    </script>
</%block>

<div class="container">
    <h1>Bienvenue sur EasyTan</h1>
    <p>Cette version du site utilise la base des horaires valable à partir du 25 août 2014</p>
    <p>Entrer le <b>nom de votre station</b>.</p>
    <%
    stop_id = "%s - %s" % (stop.stop_id, stop.stop_name) if stop else ""
    %>
    <div class="well form-inline">
        <input type="text" id="nom_station" name="stop_id" data-provide="typeahead" autocomplete="off" value="${stop_id}"/>
        <button id="sub_map" class="btn" ><i class="icon-eye-open"></i> Voir sur une carte</button>
        <button id="sub_hor" class="btn"><i class="icon-calendar"></i> Recherche horaires</button>
    </div>
    <div id="table_hor">
    </div>
</div>
