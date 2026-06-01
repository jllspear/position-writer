from datetime import datetime
from typing import Optional, Any

from sqlalchemy import Column, DateTime, Text, func
from sqlalchemy.dialects.postgresql import JSONB

from sqlmodel import SQLModel, Field


class GenericPayload(SQLModel, table=True):
    __tablename__ = "generic_payload"
    __table_args__ = {"schema": "writer"}

    id: Optional[int] = Field(default=None, primary_key=True)

    topic: str = Field(nullable=False, index=True, max_length=512)

    payload: Any = Field(sa_column=Column(JSONB, nullable=False))

    created_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now()))
