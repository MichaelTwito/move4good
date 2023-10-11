from enum import IntEnum

from pydantic import BaseModel
from datetime import datetime
from pydantic_extra_types.coordinate import Longitude, Latitude


class ReportsType(IntEnum):
    terrorists = 1
    civilians = 2


class RolesType(IntEnum):
    admin = 1
    normal = 2


class User(BaseModel):
    username: str
    password: str


class Report(BaseModel):
    description: str
    lat: Latitude
    lng: Longitude
    type: ReportsType
    id: str
    time: datetime
    report_amount: int
    
    class Config:
        arbitrary_types_allowed = True

class PartialReport(BaseModel):
    description: str
    lat: Latitude
    lng: Longitude
    type: ReportsType = 1
    report_amount: int
