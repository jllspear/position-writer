from typing import Optional
from datetime import datetime

from sqlmodel import SQLModel, Field, Column
from sqlalchemy import TIMESTAMP, Text


class DeviceLog(SQLModel, table=True):
    __tablename__ = "device_log"
    id: Optional[int] = Field(default=None, primary_key=True)
    ip: str = Field(default=None, max_length=50)
    created_at: Optional[datetime] = Field(default=None, sa_column=Column(TIMESTAMP()))
    log: str = Field(default=None, sa_column=Column(Text))
