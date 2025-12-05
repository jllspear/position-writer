from typing import Optional

from sqlmodel import SQLModel, Field, Column
from sqlalchemy import Numeric
from geoalchemy2 import Geometry


class DevicePosition(SQLModel, table=True):
    __tablename__ = "device_position"
    id: Optional[int] = Field(default=None, primary_key=True)
    ip: str = Field(default=None, max_length=50)
    base_station: str = Field(default=None, max_length=10)
    date: float = Field(default=None, sa_column=Column(Numeric()))
    coordinates: str = Field(
        default=None, sa_column=Column(Geometry("POINT", srid=4326))
    )
