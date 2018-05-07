from typing import Callable
import codecs

import paho.mqtt.client as mqtt


class MqttConnection():
    CHANNEL = 'faces'

    def __init__(self, host : str, port : str, user : str, password : str):
        self.__host = host
        self.__port = port
        self.__user = user
        self.__password = password
        self.client = None
        self.__callback = None

    def connect(self):
        self.client = mqtt.Client()

        def on_connect(client, userdata, flags, rc):
            self.client.subscribe(self.CHANNEL)

        def on_message(client, userdata, msg):
            if self.__callback is not None:
                self.__callback(msg.payload)

        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.username_pw_set(self.__user, self.__password)
        self.client.connect_async(self.__host, self.__port, 60)
        self.client.loop_start()

    def listen(self, callback: Callable[[codecs.StreamReader], None]):
        self.__callback = callback

    def send(self, channel: str, message: str):
        self.client.publish(channel, message, 2)