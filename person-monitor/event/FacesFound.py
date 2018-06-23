from typing import List

from model.User import User


class FacesFound:
    NAME = 'face_found'

    def __init__(self, image, users: List[User]) -> None:
        self.image = image
        self.users = users

    def __str__(self) -> str:
        return 'Users: '.format(self.users)