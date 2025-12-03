import json
from time import sleep

from .message_buffer import ParsedObjectBuffer
from .parser import MqttParser
from pydantic import ValidationError

from ..settings import settings


class MqttReader:
    def __init__(self, buffer: ParsedObjectBuffer, parsers: dict[str, MqttParser]):
        self.parsers = parsers
        self.buffer = buffer

    def on_message(self, client, userdata, msg):
        try:
            topic = msg.topic
            sleep(2)
            if settings.broker.verbose:
                print("Received message on topic {}".format(topic))
            payload = json.loads(msg.payload.decode("utf-8"))
            if settings.broker.verbose:
                print("Received payload {}".format(payload))
            parser = self.parsers[topic]
            parsed_element = parser.parse(payload)

            if parsed_element:
                self.buffer.add(parsed_element)

        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON message: {e}")
            return

        except ValidationError as e:
            print(f"Error processing message: {e}")
            return
