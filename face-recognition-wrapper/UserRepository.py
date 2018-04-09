from model.Face import Face
from model.User import User


class UserRepository:
    def add_user(self, user: User):
        pass

    def add_face(self, userid: str, face: Face):
        pass

    def delete_face(self, photoid: str):
        pass

    def get_user(self, photoid: str) -> User:
        return User("435", "Cici")