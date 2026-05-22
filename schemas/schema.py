from pydantic import BaseModel, field_validator
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
    id: int = Optional[int]
    name: str
    type: MeterTypeStatus
    initial_value: str
    current_value: str
    send_remote: bool = Optional[False]
    # @field_validator('send_remote')
    # @classmethod
    # def string_to_boolean(cls, v: str) -> bool:
    #     if v == 'true':
    #         return True
    #     if v == 'false':
    #         return False
    #     else:
    #         raise ValueError('Value Must be true or false string')



class SensorDeviceSchema(BaseModel):
    """Pydantic schema - sensor"""
    id: int
    name: str
    input_type: SensorTypeStatus
    initial_value: str
    current_value: str
    send_remote: bool = Optional[False]
