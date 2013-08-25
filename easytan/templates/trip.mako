<%inherit file="/base.mako"/>\
<%def name="title()">Accueil</%def>

<%block name="javascript">
</%block>

<div class="container">
    <table class="table table-striped">
        <tr><th>Heure</th><th>Arrêt</th></tr>
    % for st in trip.stop_times :
    <tr>
        <td> ${st.arrival} </td>
        <td> ${st.stop.stop_name} </td>
    </tr>
    % endfor
    </table>
</div>
