import json

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
            if settings.broker.verbose:
                print("Received message on topic {}".format(topic))

            raw = msg.payload.decode("utf-8", errors="replace")
            if settings.broker.verbose:
                print(f"Decoding payload: {repr(raw)}")

            payload = json.loads(raw)

            if settings.broker.verbose:
                print("Received payload {}".format(payload))
            parser = self.parsers[topic]
            parsed_element = parser.parse(payload)

            if parsed_element:
                if isinstance(parsed_element, (list, tuple)):
                    for el in parsed_element:
                        if el is not None:
                            self.buffer.add(el)
                else:
                    self.buffer.add(parsed_element)

        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON message: {e}")
            return

        except ValidationError as e:
            print(f"Error processing message: {e}")
            return
