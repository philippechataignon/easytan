# -*- coding: utf-8 -*-
from operator import attrgetter
from sqlalchemy import distinct, not_, or_
from sqlalchemy.orm import joinedload

from models import *

class Schedule:
    def __init__(self, session) :
        self.session = session

    @property
    def routes(self):
        return self.session.query(Route)

    @property
    def service_periods(self):
        return self.session.query(ServicePeriod)

    @property
    def service_exceptions(self):
        return self.session.query(ServiceException)

    @property
    def allstops(self):
        return self.session.query(Stop)

    @property
    def stops(self):
        return self.session.query(Stop).filter(Stop.location_type==0)

    @property
    def stations(self):
        return self.session.query(Stop).filter(Stop.location_type==1)

    @property
    def trips(self):
        return self.session.query(Trip)

    @property
    def stoptimes(self):
        return self.session.query(StopTime, Trip).join(Trip)

    @property
    def stopdir(self):
        return self.session.query(StopDir)

    def getstop(self, stop_id) :
        return self.allstops.get(stop_id)

    def service_for_date(self, service_date):
        services = set([service.service_id
            for service in self.service_periods
            if service.active_on_date(service_date)
        ])
        for item in self.service_exceptions.filter_by(date=service_date) :
            if item.exception_type == 1 :
                services.add(item.service_id)
            elif item.exception_type == 2 :
                services.discard(item.service_id)
        return services

    def stops_for_trip(self, trip) :
        l = self.session.query(StopTime).filter_by(trip=trip).order_by(StopTime.stop_sequence).all()
        return l

    def last_stop_for_trip(self, trip) :
        l = self.session.query(StopTime).filter_by(trip=trip).order_by(StopTime.stop_sequence.desc()).first()
        if l is not None :
            return l.stop

    def stop_form(self, stop_id) :
        """ Renvoit liste des stops :
        * si stop_id station (ex:LMBR) :
            renvoit [sLMBR, sLMBR1, sLMBR2]
        * si stop_id normal (ex: LMBR1) :
            renvoit [sLMBR, sLMBR1, sLMBR2]
        """
        stop = self.getstop(stop_id)
        if stop is None :
            l_stops = []
        elif stop.is_station : # cas de la station
            l_stops = stop.child_stations
        else :
            l_stops = stop.parent.child_stations

        stops  = set()
        routes = set()
        for s in l_stops :
            for sd in s.stopdir :
                stops.add(sd.stop)
                routes.add(sd.route)
        return stop, sorted(list(stops), key=attrgetter('stop_id')), sorted(list(routes), key=attrgetter('route_short_name'))

    def liste_stations(self, term) :
        q = self.session.query(Stop). options(joinedload('commune')).filter(Stop.location_type==1)
        q = q.filter(or_(Stop.stop_name.ilike('%%%s%%' % term), Stop.stop_id.ilike('%%%s%%' % term)))
        return q

    def stops_latlon(self, latl=-180, lath=180, lonl=-180, lonh=180, loc_type=None) :
        stops = self.allstops.filter(Stop.stop_lat>=latl).filter(Stop.stop_lat<=lath)
        stops = stops.filter(Stop.stop_lon>=lonl).filter(Stop.stop_lon<=lonh)
        if loc_type in (0, 1) :
            stops = stops.filter_by(location_type=loc_type)
        return stops

    def horaire(self, liste_stops, d=date.today(), route_id=None, direction_id=None) :
        if len(liste_stops) == 0 :
            return []
        liste_stop_id = [s.stop_id for s in liste_stops]

        # services actifs à la date
        services = self.service_for_date(d)
        if len(services) == 0 :
            return []

        # trajets pour la ligne et les services du jour
        # prend toutes les lignes
        trips = self.stoptimes.filter(Trip.service_id.in_(services))
        trips = trips.filter(StopTime.stop_id.in_(liste_stop_id))
        if route_id is not None :
            trips = trips.filter_by(route_id=route_id)
        if direction_id is not None :
            trips = trips.filter_by(direction_id=direction_id)
        trips = trips.order_by(StopTime.arrival_time)
        return trips
