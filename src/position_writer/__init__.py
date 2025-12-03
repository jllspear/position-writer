import importlib
from collections import defaultdict
from types import ModuleType

from sqlmodel import SQLModel

from .database.enum import CommitBehavior
from .database.writer import BatchWriter
from .mqtt.client_manager import MqttClientManager
from .mqtt.message_buffer import ParsedObjectBuffer
from .mqtt.reader import MqttReader
from .mqtt.parser import MqttParser

from .settings import settings


class PositionWriter:

    def __init__(self, parser_module: ModuleType) -> None:
        self.parser_module = parser_module

    def get_parser_from_config(self) -> dict[str, MqttParser]:
        parsers = defaultdict(MqttParser)
        for topic, parser_class_name in settings.broker.topics.items():
            parser_cls = getattr(self.parser_module, parser_class_name)
            print(f"Custom {parser_cls} found for topic {topic}")

            parsers[topic] = parser_cls()
        return parsers

    def run(self):
        parsers = self.get_parser_from_config()

        buffer = ParsedObjectBuffer[SQLModel]()

        writer = BatchWriter(buffer, CommitBehavior.COMMIT_EVERY_20_SECONDS)
        writer.start()

        reader = MqttReader(buffer, parsers)

        mqtt_client_manager = MqttClientManager(
            settings.broker, list(parsers.keys()), reader.on_message
        )
        mqtt_client_manager.connect()
        mqtt_client_manager.subscribe()
        mqtt_client_manager.loop_forever()
