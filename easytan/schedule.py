# -*- coding: utf-8 -*-
from operator import attrgetter, itemgetter
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
    def agencies(self):
        return self.session.query(Agency)

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
        stop = self.getstop(stop_id)
        if stop is None :
            return []
        elif stop.is_station : # cas de la station
            q = self.session.query(StopDir).filter(StopDir.parent_stop_id==stop_id)
        else :
            q = self.session.query(StopDir).filter(StopDir.stop_id==stop_id)
        return q

    def liste_stations(self, term) :
        q = self.session.query(Stop).filter(Stop.location_type==1)
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

if __name__ == '__main__' :
    from sqlalchemy import create_engine
    from sqlalchemy.orm import scoped_session, sessionmaker

    from connect import session
    s = Schedule(session)
    #station = s.getstop('MAI8')
    #stops = station.child_stations
    #print station, stops
    #print s.horaire(stops, date(2014,7,16)).all()
    print s.stop_form('MAI8')
    #print s.stop_form('COMM')
