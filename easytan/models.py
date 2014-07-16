from datetime import date

import sqlalchemy
from sqlalchemy.schema import Column, ForeignKey, ForeignKeyConstraint
from sqlalchemy.types import String, Integer, Float, Date, Boolean
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy.ext.declarative import declarative_base

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class ServicePeriod(Base):
    __tablename__ = "calendar"

    service_id = Column(String, primary_key=True)
    monday = Column(Boolean, nullable=False)
    tuesday = Column(Boolean, nullable=False)
    wednesday = Column(Boolean, nullable=False)
    thursday = Column(Boolean, nullable=False)
    friday = Column(Boolean, nullable=False)
    saturday = Column(Boolean, nullable=False)
    sunday = Column(Boolean, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    def __repr__(self):
        return "<ServicePeriod %s %s%s%s%s%s%s%s>" % (self.service_id,
                self.monday, self.tuesday, self.wednesday,
                self.thursday, self.friday, self.saturday, self.sunday)

    def active_on_dow(self, weekday):
        days = [self.monday, self.tuesday, self.wednesday,
            self.thursday, self.friday, self.saturday,
            self.sunday]
        return days[weekday]

    def active_on_date(self, service_date):
        within_period = (self.start_date <= service_date and service_date <= self.end_date)
        active_on_day = self.active_on_dow(service_date.weekday())
        return (within_period and active_on_day)

class ServiceException(Base):
    __tablename__ = "calendar_dates"

    service_id = Column(String, ForeignKey("calendar.service_id"), primary_key=True)
    date = Column(Date, primary_key=True)
    exception_type = Column(Integer, nullable=False)

    service_period = relationship(ServicePeriod, innerjoin=True, backref="exceptions")

    def __repr__(self):
        return "<ServiceException %s %s>" % (self.date, self.exception_type)

class Route(Base):
    __tablename__ = "routes"
    route_id = Column(String, primary_key=True)
    agency_id = Column(String)
    route_short_name = Column(String)
    route_long_name = Column(String)
    route_desc = Column(String)
    route_type = Column(Integer, nullable=False)
    route_url = Column(String)
    route_color = Column(String(6))
    route_text_color = Column(String(6))

    def __repr__(self):
        return "<Route %s>" % self.route_id

class Stop(Base):
    __tablename__ = "stops"

    stop_id = Column(String, primary_key=True)
    stop_code = Column(String)
    stop_name = Column(String, nullable=False, index=True)
    stop_desc = Column(String, ForeignKey("commune.code"), index=True)
    stop_lat = Column(Float, nullable=False)
    stop_lon = Column(Float, nullable=False)
    zone_id = Column(String)
    stop_url = Column(String)
    location_type = Column(Integer)
    parent_station = Column(String, ForeignKey("stops.stop_id"), index=True)
    parent  = relationship("Stop", backref="child_stations", remote_side=[stop_id])
    commune = relationship("Commune", innerjoin=True, backref="stations")

    def __repr__(self):
        return "<Stop %s>" % self.stop_id

    @property
    def is_station(self) :
        return self.location_type == 1

class Trip(Base):
    __tablename__ = "trips"

    trip_id = Column(String, primary_key=True)
    route_id = Column(String, ForeignKey("routes.route_id"),
                      index=True, nullable=False)
    service_id = Column(String, ForeignKey("calendar.service_id"),
                        index=True, nullable=False)
    trip_headsign = Column(String)
    trip_short_name = Column(String)
    direction_id = Column(Integer)
    block_id = Column(String)
    shape_id = Column(String)
    terminus_id = Column(String, ForeignKey("stops.stop_id"))

    route = relationship("Route", innerjoin=True, backref="trips")
    service_period = relationship("ServicePeriod", innerjoin=True, backref="trips")
    terminus   = relationship("Stop", innerjoin=True)

    def __repr__(self):
        return "<Trip %s>" % self.trip_id

class StopTime(Base):
    __tablename__ = "stop_times"

    id = Column(Integer, primary_key=True)
    trip_id = Column(String, ForeignKey("trips.trip_id"), nullable=False, index=True)
    arrival_time = Column(String(8), nullable=False)
    departure_time = Column(String(8), nullable=False)
    stop_id = Column(String, ForeignKey("stops.stop_id"),
                     index=True, nullable=False)
    stop_sequence = Column(Integer, nullable=False)
    stop_headsign = Column(String)
    pickup_type = Column(Integer)
    drop_off_type = Column(Integer)
    shape_dist_traveled = Column(String)

    trip = relationship(Trip, innerjoin=True, backref="stop_times", order_by="StopTime.stop_sequence")
    stop = relationship(Stop, innerjoin=True, backref="stop_times")

    def traite_heure(self, chaine) :
        l = chaine.split(':')
        if int(l[0]) >= 24 :
            l[0] = '%02d' % (int(l[0]) - 24)
            after = '*'
        else :
            after = ' '
        return "%s:%s%s" % (l[0], l[1], after)

    @property
    def arrival(self) :
        return self.traite_heure(self.arrival_time)

    @property
    def departure(self) :
        return self.traite_heure(self.departure_time)

    def __repr__(self):
        return "<StopTime %s %s>" % (self.trip_id, self.departure_time)


class Commune(Base) :
    __tablename__ = "commune"
    code = Column(String, primary_key=True)
    nom  = Column(String, nullable=False)

class StopDir(Base) :
    __tablename__ = "stopdir"
    parent_stop_id = Column(String, ForeignKey("stops.stop_id"))
    stop_id = Column(String, ForeignKey("stops.stop_id"), primary_key=True)
    route_id = Column(String, ForeignKey("routes.route_id"), primary_key=True)
    direction_id = Column(Integer, primary_key=True)
    routedir_id = Column(String)
    trip_headsign = Column(String, nullable=False)
    nb = Column(Integer, nullable=False)

    station = relationship("Stop", primaryjoin="StopDir.parent_stop_id==Stop.stop_id", innerjoin=True)
    stop   = relationship("Stop", primaryjoin="StopDir.stop_id==Stop.stop_id", innerjoin=True)
    route = relationship("Route", backref="stopdir", innerjoin=True)

    def __repr__(self) :
        return "<StopDir %s %s %s %s %s>" % (self.station, self.stop, self.route, self.routedir_id, self.trip_headsign)
