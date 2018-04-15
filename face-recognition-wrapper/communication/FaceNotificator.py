import os
import json
from typing import Optional
from typing import List

from communication.MqttConnection import MqttConnection
from communication.Notification import Notification
from UserRepository import UserRepository
from model.User import User
from model.Face import Face


class FaceNotificator:
    def __init__(self, mqtt: MqttConnection, user_repo: UserRepository, faces_path: str) -> None:
        self.__mqtt = mqtt
        self.__user_repo = user_repo
        self.__faces_path = faces_path

    def notify_found(self, faces: List[Face], image: str):
        for face in faces:
            user = self.__user_repo.get_user(face.id)
            self.__notify(user, face, image)

    def __notify(self, user: Optional[User], face: Face, image: str):
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
                    'image': image,
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
                'type': Notification.FACE_ADDED.value,
                'data': {
                    'user_id': user_id,
                    'face_id': face_id,
                    'file_path': file_path
                }
            }
        )
        self.__mqtt.send(MqttConnection.CHANNEL, encoded_data)

    def notify_face_deleted(self, face_id: str):
        encoded_data = json.dumps(
            {
                'type': Notification.FACE_DELETED.value,
                'data': {
                    'face_id': face_id,
                    'file_path': os.path.join(self.__faces_path, face_id + '.jpg')
                }
            }
        )
        self.__mqtt.send(MqttConnection.CHANNEL, encoded_data)