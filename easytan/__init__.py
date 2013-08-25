# -*- coding: utf8 -*-
from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from models import DBSession

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('index', '/')
    config.add_route('accueil', '/accueil')
    config.add_route('map', '/map')
    config.add_route('map_stop', '/map/{stop_id}')
    config.add_route('form_stop', '/form/{stop_id}')
    config.add_route('trip', '/trip/{trip_id}')
    config.add_route('test', '/test')
    config.add_route('test_map', '/test_map')
    config.add_route('stop_stop', '/stop/{stop_id}')
    config.add_route('savoir', '/savoir')
    config.add_route('json_stops', '/json_stops')
    config.add_route('json_hor', '/json_hor')
    config.add_route('json_api', '/json_api')
    config.add_route('json_map', '/json_map')
    config.scan()
    return config.make_wsgi_app()

