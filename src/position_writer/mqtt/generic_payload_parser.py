from typing import Any

from .parser import MqttParser
from ..database.generic_payload import GenericPayload


class GenericPayloadParser(MqttParser[GenericPayload]):

    def __init__(self, topic: str):
        self.topic = topic

    def parse(self, payload: Any) -> GenericPayload:
        return GenericPayload(topic=self.topic, payload=payload)
