# -*- coding: utf8 -*-

import re
# import urllib2
import requests
import json
from operator import attrgetter, itemgetter
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound
from datetime import date

from sqlalchemy.exc import DBAPIError
from datetime import date

from schedule import Schedule
from models import DBSession

@view_config(route_name='test', renderer='test.mako')
@view_config(route_name='savoir', renderer='savoir.mako')
def null(request) :
    return {}

@view_config(route_name='index', renderer='accueil.mako')
@view_config(route_name='accueil', renderer='accueil.mako')
@view_config(route_name='stop_stop', renderer='accueil.mako')
def accueil(request) :
    route = request.matched_route.name
    if route in ('index', 'accueil') :
        return {}
    else :
        sched = Schedule(DBSession)
        stop_id = request.matchdict.get("stop_id", "").upper()
        stop = sched.getstop(stop_id)
        return {'stop': stop}

@view_config(route_name='form_stop', renderer='form.mako')
def form(request) :
    sched = Schedule(DBSession)
    stop_id = request.matchdict.get("stop_id", "").upper()
    stop = sched.getstop(stop_id)
    q = sched.stop_form(stop_id)
    ret = calc_form(q)
    return {'stop': stop, 'date': date.today(), 'routedirs': ret['sd'], 'stops': ret['ss']}

@view_config(route_name='trip', renderer='trip.mako')
def trip(request) :
    sched = Schedule(DBSession)
    trip_id = request.matchdict.get("trip_id", "")
    return {'trip': sched.trips.get(trip_id)}

@view_config(route_name='map', renderer='map.mako')
@view_config(route_name='map_stop', renderer='map.mako')
def map(request):
    route = request.matched_route.name
    sched = Schedule(DBSession)
    if route == "map" :
        stop_id = request.params.get("stop_id", "")
        stop_id = stop_id[:4].upper()
    elif route == "map_stop" :
        stop_id = request.matchdict.get("stop_id", "").upper()
    station = sched.allstops.get(stop_id)
    if station is None :
        center = sched.allstops.get('COMM')
        zoom = 15
    else :
        center = station
        zoom = 18
    return {
        'station': station,
        'center': center,
        'zoom': zoom,
    }

### JSON
@view_config(route_name='json_stop', renderer='json')
def json_stop(request):
    sched = Schedule(DBSession)
    stop_id = request.GET.get("stop_id")
    stop = sched.getstop(stop_id)
    if stop :
        return {'id':stop.stop_id, 'name':stop.stop_name, 'commune':stop.stop_desc,
                'location_type':stop.location_type, 'parent_station': stop.parent_station,
                'lat': stop.stop_lat, 'long': stop.stop_lon,
            }
    else :
        return {'id':None, 'name':None, 'commune':None,
                'location_type':None, 'parent_station': None,
                'lat': None, 'long': None,
            }

@view_config(route_name='json_stops', renderer='json')
def json_stops(request):
    sched = Schedule(DBSession)
    term = request.GET.get("query")
    # minimum 2 caractères pour renvoyer
    if len(term) < 2 :
        return []
    else :
        return [{'id':s.stop_id, 'name':s.stop_name, 'commune':s.stop_desc} for s in sched.liste_stations(term)]

@view_config(route_name='json_hor', renderer='json')
def json_hor(request):
    sched = Schedule(DBSession)
    stop_id = request.GET.get("stop_id").strip().upper()
    stop = sched.getstop(stop_id)
    if stop is None :
        data = {}
    else :
        if stop.is_station :
            liste_stops = stop.child_stations
        else :
            liste_stops = [stop]
        d = request.GET.get("date")
        if d is None :
            ddate = date.today()
        else :
            d = d.replace('-','')
            ddate = date(int(d[4:8]), int(d[2:4]), int(d[0:2]))
        routedir_id = request.GET.get("routedir_id")
        if routedir_id is None or routedir_id == 'ALL' :
            route_id = None
            direction_id = None
        else:
            route_id, direction_id = routedir_id.split('#')
        trips = sched.horaire(liste_stops, d=ddate, route_id=route_id, direction_id=direction_id)
        data = [{'heure': h.departure,
            'ligne': t.route.route_short_name,
            'sens': 'gauche' if t.direction_id == 1 else 'droite',
            'terminus': t.terminus.stop_name,
            'stop': h.stop_id,
            'trip_id': t.trip_id
            } for (h, t) in trips]
    head =['Heure', 'Ligne', 'Sens', 'Terminus', 'Arrêt']
    return {'head':head, 'data':data}

@view_config(route_name='json_map', renderer='json')
def json_map(request):
    sched = Schedule(DBSession)
    latl = request.GET.get("latl", -180)
    lath = request.GET.get("lath", 180)
    lonl = request.GET.get("lonl", -180)
    lonh = request.GET.get("lonh", +180)
    zoom = int(request.GET.get("zoom", -1))
    loc_type = 0 if zoom >= 18 else 1 ;
    stops = sched.stops_latlon(latl=latl, lath=lath, lonl=lonl, lonh=lonh, loc_type=loc_type)
    l = [{'lat': s.stop_lat, 'lon': s.stop_lon, 'id': s.stop_id, 'nom': s.stop_name, 'loc_type':s.location_type} for s in stops]
    return l

def calc_form(q):
    qq = q.all()
    ld = [(l.route_id, l.direction_id, l.trip_headsign, l.route.route_short_name) for l in qq]
    sd = sorted(set(ld), key=itemgetter(0,1))
    ss = sorted(set([l.stop_id for l in qq]))
    return {'sd': sd, 'ss': ss}

@view_config(route_name='json_form', renderer='json')
def json_form(request):
    sched = Schedule(DBSession)
    stop_id = request.GET.get("stop_id")
    q = sched.stop_form(stop_id)
    ret = calc_form(q)
    sd = ret['sd']
    return [{'route_id':s[0], 'direction_id':s[1], 'trip_headsign': s[2], 'route_short_name': s[3]}
            for s in sorted(sd, key=itemgetter(0,1))]

@view_config(route_name='json_trip', renderer='json')
def json_trip(request):
    sched = Schedule(DBSession)
    trip_id = request.GET.get("trip_id")
    trip = sched.trips.get(trip_id)
    l = [{"arrival": st.arrival, "stop_name": st.stop.stop_name, "stop_id": st.stop.stop_id} for st in trip.stop_times]
    return l

@view_config(route_name='json_api', renderer='json')
def json_api(request) :
    stop_id = request.GET.get("stop_id")
    if stop_id is None :
        return {'head':'No stop_id', 'data':[]}
    url = "http://open.tan.fr/ewp/tempsattente.json/%s" % stop_id.upper()
    r = requests.get(url)
    head =['Temps', 'Ligne', 'Sens', 'Direction', 'Arrêt']
    return {'head':head, 'data':r.json()}
