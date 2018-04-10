import json

from communication.MqttConnection import MqttConnection


class NotificationListener:
    def __init__(self, connection: MqttConnection) -> None:
        self.__connection = connection
        self.__callback = None
        self.__type = None

    def listen(self, callback, type: str):
        self.__callback = callback
        self.__type = type
        self.__connection.listen(self.__prepare)

    def __prepare(self, message):
        data = json.loads(message.decode())
        if data['type'] != self.__type:
            return
        self.__callback(data['data']['user_id'], data['data']['face_id'], data['data']['file_path'])