from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
import datetime

Base = declarative_base()

class ReportInfrared(Base):
    """Infrared Report"""

    __tablename__ = "report_infrared"

    sensor_id = Column(String(100), nullable=False)
    status_code = Column(Integer, nullable=False)
    temperature = Column(Integer, nullable=False)
    timestamp = Column(String(100), nullable=False)
    date_created = Column(DateTime, primary_key=True)
    trace_id = Column(String(100), nullable=False)

    def __init__(self, sensor_id, status_code, temperature, timestamp, trace_id):
        """Initialize a Patrol Report"""
        self.sensor_id = sensor_id
        self.status_code = status_code
        self.temperature = temperature
        self.timestamp = timestamp
        self.date_created = datetime.datetime.now()
        self.trace_id = trace_id

    def to_dict(self):
        dict = {}
        dict['sensor_id'] = self.sensor_id
        dict['status_code'] = self.status_code
        dict['temperature'] = self.temperature
        dict['timestamp'] = self.timestamp
        dict['date_created'] = self.date_created
        return dict

class ReportPatrol(Base):
    """Patrol Report"""

    __tablename__ = "report_patrol"

    officer_id = Column(Integer, nullable=False)
    reporter = Column(String(100), nullable=False)
    status_code = Column(Integer, nullable=False)
    timestamp = Column(String(100), nullable=False)
    writeup = Column(String(250), nullable=False)
    date_created = Column(DateTime, primary_key=True)
    trace_id = Column(String(100), nullable=False)
    
    def __init__(self, officer_id, reporter, status_code, timestamp, writeup, trace_id):
        self.officer_id = officer_id
        self.reporter = reporter
        self.status_code = status_code
        self.timestamp = timestamp
        self.writeup = writeup
        self.date_created = datetime.datetime.now()
        self.trace_id = trace_id

    def to_dict(self):
        dict = {}
        dict['officer_id'] = self.officer_id
        dict['reporter'] = self.reporter
        dict['status_code'] = self.status_code
        dict['timestamp'] = self.timestamp
        dict['writeup'] = self.writeup
        dict['date_created'] = self.date_created
        return dict