import time
from collections import defaultdict
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Callable

import paho.mqtt.client as mqtt

from ..settings.broker import BrokerSettings


class MqttClientManager:
    def __init__(
        self, settings: BrokerSettings, topics: list[str], on_message: Callable
    ):
        self._id = 0
        self.topics = topics
        self.on_message = on_message
        self.settings = settings
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.pending_subscriptions = defaultdict(str)
        self.executor = ThreadPoolExecutor(max_workers=5)

    def on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            print(f"Connected to {self.settings.url} MQTT Broker !")
        else:
            print(
                f"Failed to connect to server {self.settings.url}, return code {reason_code}"
            )

    def connect(self):
        self._id += 1

        if self.client:
            self.client.loop_stop()
            self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

        self.client.enable_logger()
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.username_pw_set(self.settings.username, self.settings.password)
        self.client.connect(self.settings.url, self.settings.port)

    def on_disconnect(self, client, userdata, flags, reason_code, properties):
        print(f"{self.settings.url} disconnected with result code: {reason_code}")

        reconnect_count = 0
        reconnect_delay = self.settings.first_reconnect_delay
        while reconnect_count < self.settings.max_reconnect_count:
            print(f"{self.settings.url} reconnecting in {reconnect_delay} seconds...")
            time.sleep(reconnect_delay)

            try:
                self.connect()
                self.subscribe()
                print(f"{self.settings.url} reconnected successfully!")
                self.client.loop_forever()
                return
            except Exception as err:
                print(
                    f"{self.settings.url} reconnect failed with error {err}. Retrying..."
                )

            reconnect_delay *= self.settings.reconnect_rate
            reconnect_delay = min(reconnect_delay, self.settings.max_reconnect_delay)
            reconnect_count += 1
        print(
            f"{self.settings.url} reconnect failed after {reconnect_count} attempts. Exiting..."
        )
        self.client.loop_stop()

    def on_subscribe(self, client, userdata, mid, reason_code_list, properties):
        topic = self.pending_subscriptions.pop(mid)

        if reason_code_list[0].is_failure:
            print(f"Failed to connect to {topic} on {self.settings.url}")
            return
        print(
            f"Connected to topic {topic} on {self.settings.url} MQTT Broker! You be granted the following QoS: {reason_code_list[0].value}"
        )

    def subscribe(self):
        self.client.on_message = self.process_on_message
        self.client.on_subscribe = self.on_subscribe
        for topic in self.topics:
            result, mid = self.client.subscribe(topic)
            self.pending_subscriptions[mid] = topic

    def process_on_message(self, client, userdata, msg):
        self.executor.submit(self.on_message, client, userdata, msg)

    def loop_forever(self):
        self.client.loop_forever()
