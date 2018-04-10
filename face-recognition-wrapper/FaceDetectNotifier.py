from typing import List

from UserRepository import UserRepository
from communication.FaceNotificator import FaceNotificator
from model.Face import Face


class FaceDetectNotifier:
    def __init__(self, face_notificator: FaceNotificator, user_repo: UserRepository) -> None:
        self.__face_notificator = face_notificator
        self.__user_repo = user_repo

    # given a list of face objects notifies found for each face using FaceNotificator
    def notify(self, faces: List[Face]):
        for face in faces:
            user = self.__user_repo.get_user(face.id)
            self.__face_notificator.notify_found(user, face)