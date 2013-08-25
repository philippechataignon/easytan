<%inherit file="/base.mako"/>\
<%def name="title()">Accueil</%def>

<%block name="header">
    <link href="/static/bootstrap/css/datepicker.css" rel="stylesheet">
</%block>

<%block name="javascript">
    <script src="/static/bootstrap/js/bootstrap-datepicker.js"></script>
    <script src="/static/bootstrap/js/locales/bootstrap-datepicker.fr.js"></script>
    <script type="text/javascript">
    $(function() {
        $('#sub_hor').click(function() {
            $.getJSON(
                '/json_hor', 
                {
                    'stop_id': $('#stop_id option:selected').val(),
                    'route_id':$('#route_id option:selected').val(),
                    'direction_id':$('#direction_id option:selected').val(),
                    'date': $('#date').val(),
                }, 
                function(data) {
                    var table=['<table class="table table-striped"><tr>'];
                    $.each(data.head, function(key, item){
                        table.push('<th>'+item+'</th>');
                    });
                    table.push('</tr>');
                    $.each(data.data, function(key, item){
                        table.push('<tr>');
                        table.push('<td><a href="/trip/'+item.trip_id+'">'+item.heure+'</a></td>');
                        table.push('<td><img width="25" height="25" src="/static/images/lignes/'+item.ligne+'.gif"></td>');
                        table.push('<td><img width="10" height="10" src="/static/images/'+item.sens+'.gif"></td>');
                        table.push('<td>'+item.terminus+'</td>');
                        table.push('<td><a href="/map/'+item.stop+'">'+item.stop+'</a></td>');
                        table.push('</tr>');
                    });
                    table.push('</table>');
                $('#table_hor').html(table.join(''));  
                }
            );
        })
        $('#date').datepicker({
            'language': 'fr',
            'format': 'dd-mm-yyyy',
            'weekStart':1,
            }).datepicker('setValue', '${date.strftime("%d-%m-%Y")}');
    });
    </script>
</%block>
% if stop is not None :
<%
stop_id = "%s - %s (%s)" % (stop.stop_id, stop.stop_name, stop.commune.nom) if stop else ""
%>
<div class="container">
    <h2>Horaires ${stop_id}</h2>
    <div class="well form-inline">
        Arrêt:
        <select class="span2" name="stop_id" id="stop_id">
            <option value=${stop.stop_id} selected="selected">Tous</option>
        % for s in stops:
            <option value="${s.stop_id}"
            %if s.stop_id == stop.stop_id :
                selected="selected"
            %endif
            >${s.stop_id}</option>
        % endfor
        </select>
        Ligne:
        <select class="span2" name="route_id" id="route_id">
            <option value="ALL" selected="selected">Toutes les lignes</option>
        % for r in routes:
            <option value="${r.route_id}">${r.route_long_name}</option>
        % endfor
        </select>
        Sens:
        <select class="span1" name="direction_id" id="direction_id">
            <option value="ALL" selected="selected">&larr;&nbsp;&rarr;</option>
            <option value="0">&rarr;</option>
            <option value="1">&larr;<img width="10" height="10" src="/static/images/droite.gif"></option>
        </select>
        Date:
        <input type="text" class="span2" id="date" name="textdate" value="${date.strftime("%d-%m-%Y")}"/>
        <button id="sub_hor" class="btn">Valider</button>
    </div>
    <div id="table_hor" />
</div>
% else :
<div class="container">
    Station inconnue
</div>
%endif

