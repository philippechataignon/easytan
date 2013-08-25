from datetime import date

import sqlalchemy
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey, ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import String, Integer, Float, Date, Boolean

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class ShapePoint(Base):
    __tablename__ = "shapes"

    id = Column(Integer, primary_key=True)
    shape_id = Column(String, index=True)
    shape_pt_lat = Column(Float, nullable=False)
    shape_pt_lon = Column(Float, nullable=False)
    shape_pt_sequence = Column(Integer, nullable=False)
    shape_dist_traveled = Column(String)

    def __repr__(self):
        return "<ShapePoint #%s (%s, %s)>" % (self.shape_pt_sequence,
                                              self.shape_pt_lat,
                                              self.shape_pt_lon)


class Agency(Base):
    __tablename__ = "agency"
    agency_id = Column(String, primary_key=True)
    agency_name = Column(String, nullable=False)
    agency_url = Column(String, nullable=False)
    agency_timezone = Column(String, nullable=False)
    agency_lang = Column(String(2))
    agency_phone = Column(String)

    def __repr__(self):
        return "<Agency %s>" % self.agency_id

    def __init__(self, **kwargs):
        Entity.__init__(self, **kwargs)

        if not hasattr(self, "agency_id") or self.agency_id is None:
            self.agency_id = "__DEFAULT__"


class ServicePeriod(Base):
    __tablename__ = "calendar"

    service_id = Column(String, primary_key=True)
    # new_id = Column(String)
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
                                                      self.monday,
                                                      self.tuesday,
                                                      self.wednesday,
                                                      self.thursday,
                                                      self.friday,
                                                      self.saturday,
                                                      self.sunday)

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
    # new_id = Column(String)

    service_period = relationship(ServicePeriod, innerjoin=True, backref="exceptions")

    def __repr__(self):
        return "<ServiceException %s %s>" % (self.date, self.exception_type)


class Route(Base):
    __tablename__ = "routes"
    route_id = Column(String, primary_key=True)
    agency_id = Column(String, ForeignKey("agency.agency_id"), index=True)
    route_short_name = Column(String)
    route_long_name = Column(String)
    route_desc = Column(String)
    route_type = Column(Integer, nullable=False)
    route_url = Column(String)
    route_color = Column(String(6))
    route_text_color = Column(String(6))
    # new_id   = Column(String)

    agency = relationship("Agency", innerjoin=True, backref="routes")

    def __repr__(self):
        return "<Route %s>" % self.route_id

    def __init__(self, **kwargs):
        Entity.__init__(self, **kwargs)

        if not hasattr(self, "agency_id") or self.agency_id is None:
            self.agency_id = "__DEFAULT__"


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

    @property
    def uses_frequency(self):
        #would be even better to use EXISTS here since the actual count is irrelevant
        return Frequency.query.with_parent(self).count() > 0


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

class Fare(Base):
    __tablename__ = "fare_attributes"

    fare_id = Column(String, primary_key=True)
    price = Column(String, nullable=False)
    currency_type = Column(String(3), nullable=False)
    payment_method = Column(Integer, nullable=False)
    transfers = Column(Integer)
    transfer_duration = Column(Integer)

    def __repr__(self):
        return "<Fare %s %s>" % (self.price, self.currency_type)


class FareRule(Base):
    __tablename__ = "fare_rules"

    id = Column(Integer, primary_key=True)
    fare_id = Column(String, ForeignKey("fare_attributes.fare_id"),
                     index=True, nullable=False)
    route_id = Column(String, ForeignKey("routes.route_id"), index=True)
    origin_id = Column(String)
    destination_id = Column(String)
    contains_id = Column(String)

    fare = relationship(Fare, innerjoin=True, backref="rules")
    route = relationship(Route, innerjoin=True, backref="fare_rules")


class Frequency(Base):
    __tablename__ = "frequencies"

    id = Column(Integer, primary_key=True)
    trip_id = Column(String, ForeignKey("trips.trip_id"),
                     index=True, nullable=False)
    start_time = Column(String(8), nullable=False)
    end_time = Column(String(8), nullable=False)
    headway_secs = Column(Integer, nullable=False)

    trip = relationship(Trip, innerjoin=True, backref="frequencies")

    def __repr__(self):
        return "<Frequency %s-%s %s>" % (self.start_time, self.end_time,
                                         self.headway_secs)

    @property
    def trip_times(self):
        out = []
        start_time = self.start_time.val
        end_time = self.end_time.val
        time = start_time
        while time < end_time:
            out.append(time)
            time += self.headway_secs
        return out


class Transfer(Base):
    __tablename__ = "transfers"

    id = Column(Integer, primary_key=True)
    from_stop_id = Column(String, ForeignKey("stops.stop_id"),
                          index=True, nullable=False)
    to_stop_id = Column(String, ForeignKey("stops.stop_id"),
                        index=True, nullable=False)
    transfer_type = Column(Integer, nullable=False)
    min_transfer_time = Column(String)

    from_stop = relationship(Stop,
                             primaryjoin="Transfer.from_stop_id==Stop.stop_id",
                             backref="transfers_away")
    to_stop = relationship(Stop,
                           primaryjoin="Transfer.to_stop_id==Stop.stop_id",
                           backref="transfers_from")

class Commune(Base) :
    __tablename__ = "commune"
    code = Column(String, primary_key=True)
    nom  = Column(String, nullable=False)

class StopDir(Base) :
    __tablename__ = "stopdir"

    stop_id = Column(String, ForeignKey("stops.stop_id"), primary_key=True)
    route_id = Column(String, ForeignKey("routes.route_id"), primary_key=True)
    direction_id = Column(Integer, primary_key=True)
    terminus_id = Column(String, ForeignKey("stops.stop_id"), nullable=False)
    nb = Column(Integer, nullable=False)

    stop   = relationship("Stop", primaryjoin="StopDir.stop_id==Stop.stop_id", backref="stopdir", innerjoin=True)
    route = relationship("Route", backref="stopdir", innerjoin=True)
    terminus   = relationship("Stop", primaryjoin="StopDir.terminus_id==Stop.stop_id", innerjoin=True)

    def __repr__(self) :
        return "<StopDir %s %s %s %s>" % (self.stop, self.route, self.direction_id, self.terminus) 
