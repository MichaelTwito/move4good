from enum import IntEnum
from pydantic import BaseModel
from datetime import datetime
from pydantic_extra_types.coordinate import Longitude, Latitude


class RolesType(IntEnum):
    admin = 1
    normal = 2

class User(BaseModel):
    username: str
    password: str

class DeliveryCenter(BaseModel):
    lat: Longitude
    lng: Latitude
    
class Order(BaseModel):
    contact_number: str
    size_description: str
    status: int
    dropoff_lat: Longitude
    dropoff_lng: Latitude
    created_at: datetime
    last_updated_at: datetime
    delivery_center_id: str
    delivery_center: DeliveryCenter
    
    class Config:
        arbitrary_types_allowed = True

# class PartialReport(BaseModel):
#     description: str
#     lat: Latitude
#     lng: Longitude
#     type: ReportsType = 1
#     report_amount: int
