import importlib
from collections import defaultdict
from sqlmodel import SQLModel

from database.enum import CommitBehavior
from database.writer import BatchWriter
from mqtt.client_manager import MqttClientManager
from mqtt.message_buffer import ParsedObjectBuffer
from mqtt.reader import MqttReader
from mqtt.parser import MqttParser

from settings import settings


def get_parser_from_config(parser_module: str) -> dict[str, MqttParser]:
    parsers = defaultdict(MqttParser)
    for topic, parser_class_name in settings.broker.topics.items():
        parser_module = importlib.import_module(parser_module)
        parser_cls = getattr(parser_module, parser_class_name)
        print(f"Custom {parser_cls} found for topic {topic}")

        parsers[topic] = parser_cls()
    return parsers


def run_broker_to_db_app(parser_module: str):
    parsers = get_parser_from_config(parser_module)

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
