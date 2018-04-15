import json

from communication.MqttConnection import MqttConnection
from communication.Notification import Notification


class NotificationListener:
    def __init__(self, connection: MqttConnection) -> None:
        self.__connection = connection
        self.__callback_by_type = {}

    def listen(self, type: str, callback):
        self.__callback_by_type[type] = callback
        self.__connection.listen(self.__prepare)

    def __prepare(self, message):
        data = json.loads(message.decode())
        callback_type = data['type']
        if callback_type not in self.__callback_by_type:
            return
        if callback_type == Notification.FACE_ADDED.value:
            self.__callback_by_type[callback_type]\
                (data['data']['user_id'], data['data']['face_id'], data['data']['file_path'])
        elif callback_type == Notification.FACE_DELETED.value:
            self.__callback_by_type[callback_type](data['data']['file_path'])