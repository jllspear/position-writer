from typing import Optional, Any
from pydantic import BaseModel, Field, field_validator, ConfigDict

from position_writer.database.custom_models import DevicePosition
from position_writer.mqtt.parser import MqttParser


class DevicePositionParser(MqttParser[DevicePosition]):
    def parse(self, payload: Any) -> Optional[DevicePosition]:
        validated_data = DevicePositionValidator(**payload)

        coordinates_wkt = f"POINT({validated_data.lon} {validated_data.lat})"

        return DevicePosition(
            ip=validated_data.ip,
            base_station=validated_data.base_station,
            date=validated_data.date,
            coordinates=coordinates_wkt,
        )


class DevicePositionValidator(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)

    ip: str = Field(
        ...,
        max_length=50,
        pattern=r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$|^[a-zA-Z0-9\-\.]+$",
    )
    base_station: str = Field(..., max_length=10)
    date: Optional[float] = Field(None, ge=0)
    lat: float = Field(..., ge=-90, le=90, description="Latitude (mandatory)")
    lon: float = Field(..., ge=-180, le=180, description="Longitude (mandatory)")

    @field_validator("date", mode="before")
    @classmethod
    def validate_date(cls, v):
        if v is None:
            return v
        if isinstance(v, (int, float)):
            return float(v)
        if isinstance(v, str):
            try:
                return float(v)
            except ValueError:
                raise ValueError("Date must be a numeric timestamp")
        return v
