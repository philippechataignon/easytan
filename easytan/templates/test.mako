<%inherit file="/base.mako"/>\
<%def name="title()">Test</%def>

<%block name="javascript">
    <script type="text/javascript">
    $.getJSON('/json_hor?stop_id=PIRM&date=20120902&route=94-0&direction=1', function(data) {
        var table='<table class="table table-striped"><tr>';
        $.each(data.head, function(key, item){
            table+='<th>'+item+'</th>';
        });
        table += '</tr>';
        $.each(data.data, function(key, item){
            table+='<tr>';
            $.each(item, function(key, item){
                table+='<td>'+item+'</td>';
            });
            table+='</tr>';
        });
        table+='</table>';
        $("#content").html(table);  
    });
    </script>
</%block>
<div id="content" />
