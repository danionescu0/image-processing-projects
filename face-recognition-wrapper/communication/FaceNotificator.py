import json
from typing import Optional


from communication.MqttConnection import MqttConnection
from communication.Notification import Notification
from model.Face import Face
from model.User import User


class FaceNotificator:
    def __init__(self, mqtt: MqttConnection) -> None:
        self.__mqtt = mqtt

    def notify_found(self, user: Optional[User], face: Face):
        user_id = None
        user_name = None
        if user is not None:
            user_id = user.id
            user_name = user.name

        encoded_data = json.dumps(
            {
                'type': Notification.FACE_FOUND.value,
                'data': {
                    'user_id': user_id,
                    'user_name': user_name,
                    'top_px': face.top,
                    'right_px': face.right,
                    'bottom_px': face.bottom,
                    'left_px': face.left
                }
            }
        )
        self.__mqtt.send(MqttConnection.CHANNEL, encoded_data)

    def notify_added(self, user_id: str, face_id: str, file_path: str):
        encoded_data = json.dumps(
            {
                'type': Notification.FACE_PROCESSED.value,
                'data': {
                    'user_id': user_id,
                    'face_id': face_id,
                    'file_path': file_path
                }
            }
        )
        self.__mqtt.send(MqttConnection.CHANNEL, encoded_data)

    def notify_deleted(self):
        pass