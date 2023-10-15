import json
from enum import Enum, IntEnum
from pydantic import BaseModel
from typing import Optional as OptionalType
from pydantic_extra_types.coordinate import Longitude, Latitude


class RolesType(IntEnum):
    admin = 1
    normal = 2

class User(BaseModel):
    username: str
    password: str


class StatusEnum(Enum):
    OPENED = 'opened'
    ASSIGNED = 'volunteer_assigned'
    PICKED_UP = 'picked_up'
    COMPLETE = 'completed'

class DeliveryCenter(BaseModel):
    name: str
    address: str
    lat: Longitude
    lng: Latitude
    
class Order(BaseModel):
    contact_number: str
    size_description: str
    description: OptionalType[str] = None
    dropoff_address: str
    dropoff_lat: Longitude
    dropoff_lng: Latitude
    delivery_center_id: str

    
    class Config:
        arbitrary_types_allowed = True

class UpdateOrderModel(BaseModel):
    contact_number: OptionalType[str] = None
    size_description: OptionalType[str] = None
    dropoff_address: OptionalType[str] = None
    status: OptionalType[StatusEnum] = None
    description: OptionalType[str] = None
    dropoff_lat: OptionalType[Longitude] = None
    dropoff_lng: OptionalType[Latitude] = None
    delivery_center_id: OptionalType[str] = None