<%inherit file="/base.mako"/>\
<%def name="title()">En savoir plus</%def>

<div class="container">
    <div class="row">
        <div class="span4">
            <h2>Pourquoi easytan</h2>
            <p><a href="/">easytan.fr</a> est né de l'idée d'obtenir les horaires des bus de la TAN
            passant à un arrêt donné, quelque soit la ligne.</p>
            <p>Pour connaître tous les passages à une station, il suffit de taper son nom
            dans la page d'accueil. On peut ensuite affiner en filtrant sur un des arrêts de la
            station</p>
        </div>
        <div class="span4">
            <h2>Station, arrêt</h2>
            <p>Une station correspond à un nom. Exemple : Commerce.</p>
            <p>Une station possède plusieurs arrêts qui correspondent aux différents
            emplacements physiques où l'on peut accéder au bus/busway/tramway</p>
            <p> En général, une station possède au minumum 2 arrêts, un dans chaque sens.</p>
        </div>
        <div class="span4">
            <h2>GTFS et Opendata</h2>
            <p>Les horaires de ce site s'appuie sur les données mises en ligne
            sur le site <a href="http://data.nantes.fr">data.nantes.fr</a> et, plus particulièrement
            le jeu de données TAN
            </p>
            <p>Ce jeu de données est au format <a href="https://developers.google.com/transit/gtfs/reference">GTFS</a>, ce qui
            permet de disposer d'outils construits autour de ce standard.
            </p>
        </div>
    </div>
    <div class="row">
        <div class="span4">
            <h2>Astuce easytan</h2>
            <p>Une fois que l'on a repéré le code de l'arrêt, on peut mettre directement le lien
            dans les favoris.</p>
            <p>Exemple : la station <i>Ruette</i> a deux arrêts : RUET1 et RUET2. Pour obtenir directement
            les horaires du jour à cet arret, on peut mettre l'adresse suivante en favori :<br />
            <code><a href="http://easytan.fr/stop/RUET2">http://easytan.fr/stop/RUET2</a>
            </code>
            </p>
        </div>
        <div class="span4">
            <h2>Outils utilisés</h2>
            <p>Le site est développé est utilisant <a href="http://twitter.github.com/bootstrap/index.html">Bootstrap</a>
            pour le style HTML, CSS et Javascript.</p>
            <p>Le jeu de données GTFS a été chargé par <a href="http://www.sqlalchemy.org/">SQLAlchemy</a> pour
            être indépendant de la base de données utilisée. Pour l'instant, easytan.fr tourne avec
            une base de données <a href="http://www.sqlite.org/">SQLite</a>.
            <p>Le framework retenu est <a href="http://www.pylonsproject.org">Pyramid</a> qui fonctionne sous
            <a href="http://www.python.org">Python</a>.</p>
            <p>Le serveur Web tourne sous <a href="http://nginx.org">nginx</a> avec 
            <a href="http://projects.unbit.it/uwsgi">uwsgi</a>
            pour faire le lien avec Pyramid.</p>
        </div>
        <div class="span4">
            <h2>Contact</h2>
            <p>Un avis, des remarques : envoyer un mail à
            <a href="mailto:webmaster@easytan.fr">webmaster@easytan.fr</a>
            </p>
        </div>
    </div>
</div>
