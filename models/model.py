from sqlalchemy import Column, Integer, String, Text, Boolean, URL, Enum as UNIEnum
from dbapi.deps import Base
from enum import Enum
from sqlalchemy_utils import URLType



class MeterTypeStatus(str, Enum):
    """Choices for meter device"""
    cold_water = "холодная вода"
    hot_water = "горячая вода"
    electricity = "электричество"
    heat_metering = "тепловая энергия"
    gas_fluid = "природный газ"

class SensorTypeStatus(str, Enum):
    """Choices for Sensor INPUT/OUTPUT"""
    allways_open = "NO"
    allways_closed = "NC"
    analog_input = "Analog input"
    resistance = "Resistance"
    digital_a = "Input A"
    digital_b = "Input B"



class UserDataModel(Base):
    """ORM model - userdata
    login: str
    password: str
    address: str
    token: str
    remote_url: str_url
    """
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, index=True)
    password = Column(Text, index=True)
    address = Column(Text, index=True)
    token = Column(Text, index=True)
    remote_url = Column(URLType, index=True, default='http://localhost') 


class MeteringDeviceModel(Base):
    """ORM Model - metering device
    id: int
    name: str
    type: enum
    initial_value: str
    current_value: str
    send_remote: str
    """
    __tablename__ = "meter"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(UNIEnum(MeterTypeStatus), index=True, default=MeterTypeStatus.electricity)
    initial_value = Column(Text, index=True)
    current_value = Column(Text, index=True)
    send_remote = Column(Boolean,default=False)


class SensorDeviceModel(Base):
    """ORM Model - sensor device
    id: int
    name: str
    input_type: enum
    initial_value: str
    current_value: str
    send_remote: str
    """
    __tablename__ = "sensor"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    input_type = Column(UNIEnum(SensorTypeStatus), index=True, default=SensorTypeStatus.allways_open)
    initial_value = Column(Text, index=True)
    current_value = Column(Text, index=True)
    send_remote = Column(Boolean,default=False)
