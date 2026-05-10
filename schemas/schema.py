from pydantic import BaseModel
from typing import List, Optional
from models.model import MeterTypeStatus, SensorTypeStatus



# Схемы получения типизированных данных

class UserDataSchema(BaseModel):
    """Pydantic схема для получения данных"""
    id: int
    login: str
    password: str
    address: str
    token: str
    remote_url: str

class UserLoginSchema(BaseModel):
    """Pydantic схема для получения данных"""
    login: str
    password: str

class MeteringDeviceSchema(BaseModel):
    """Pydantic схема для получения данных"""
    id: int
    name: str
    type: MeterTypeStatus
    initial_value: str
    current_value: str
    send_remote: bool = Optional[False]


class SensorDeviceSchema(BaseModel):
    """Pydantic schema - sensor"""
    id: int
    name: str
    input_type: SensorTypeStatus
    initial_value: str
    current_value: str
    send_remote: bool = Optional[False]
