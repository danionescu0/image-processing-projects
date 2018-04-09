import json
from typing import List
from typing import Optional

from MqttConnection import MqttConnection
from UserRepository import UserRepository
from model.Face import Face
from model.User import User


class FaceDetectNotifier:
    def __init__(self, mqtt: MqttConnection, user_repo: UserRepository) -> None:
        self.__mqtt = mqtt
        self.__user_repo = user_repo

    def notify(self, faces: List[Face]):
        for face in faces:
            user = self.__user_repo.get_user(face.id)
            self.__mqtt.send(MqttConnection.FACES_CHANNEL, self.__format_for_mqtt(user, face))

    def __format_for_mqtt(self, user: Optional[User], face: Face):
        user_id = None
        user_name = None
        if user is not None:
            user_id = user.id
            user_name = user.name

        return json.dumps(
            {
                'user_id' : user_id,
                'user_name' : user_name,
                'top_px' : face.top,
                'right_px' : face.right,
                'bottom_px' : face.bottom,
                'left_px' : face.left,
            }
        )