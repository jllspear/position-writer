from position_writer.database.custom_models import DeviceLog
from position_writer.mqtt.parser import MqttParser

from typing import Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict


class DeviceLogParser(MqttParser[DeviceLog]):
    def parse(self, payload: any) -> DeviceLog:
        validated_data = DeviceLogValidator(**payload)

        return DeviceLog(
            ip=validated_data.ip,
            log=validated_data.log,
        )


class DeviceLogValidator(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)

    ip: str = Field(
        None,
        max_length=50,
        pattern=r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$|^[a-zA-Z0-9\-\.]+$",
    )
    created_at: Optional[int] = None
    log: str = Field(None, max_length=10000)

    @classmethod
    @field_validator("log", mode="before")
    def validate_log(cls, v):
        if v is None:
            return v
        return str(v)
