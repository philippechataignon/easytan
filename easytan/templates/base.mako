<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="utf-8">
    <title>EasyTan | ${self.title()}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Horaires Tan Nantes">
    <meta name="keywords" content="horaire, horaires, nantes, bus, busway,tramway, tan">
    <meta name="author" content="Corentin Chataignon">
    <meta name="author" content="Philippe Chataignon">
    <link href="/static/bootstrap/css/bootstrap.css" rel="stylesheet">
    <link href="/static/bootstrap/css/bootstrap-responsive.css" rel="stylesheet">
    <style>
        body { padding-top: 60px; }
    </style>
    <%block name="header" />
</head>

<body>
<div class="navbar navbar-fixed-top">
    <div class="navbar-inner">
        <div class="container">
            <a class="brand" href="/">EasyTan</a>
            <ul class="nav">
                <li><a href="/">Accueil</a></li>
                <li><a href="/savoir">En savoir plus</a></li>
            </ul>
        </div>
    </div>
</div>
${self.body()}
<!-- include Javascript -->
    <script src="/static/js/jquery.min.js"></script>
    <%block name="javascript" />
<!-- fin include Javascript -->
</body>
</html>
