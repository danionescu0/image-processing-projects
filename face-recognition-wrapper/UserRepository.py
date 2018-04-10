from typing import Optional

from pymongo import MongoClient

from model.User import User


class UserRepository:
    DATABASE_NAME = 'face_detect'
    COLLECTION_NAME = 'users'

    def __init__(self, host_uri: str) -> None:
        self.__host_uri = host_uri
        self.__collection = {}

    def add_user(self, user: User):
        update_data = {
            "$set" : {
                "name": user.name,
            }
        }
        self.get_collection(self.COLLECTION_NAME)\
            .update_one({"_id": user.id}, update_data, True)

    def add_face(self, face_id: str, userid: str):
        update_data = {
            "$addToSet" : {
                "faces": face_id
            }
        }
        self.get_collection(self.COLLECTION_NAME)\
            .update_one({"_id": userid}, update_data, True)

    def delete_face(self, photoid: str):
        pass

    def get_user(self, photoid: str) -> Optional[User]:
        if not photoid:
            return None
        user = self.get_collection(self.COLLECTION_NAME)\
            .find_one({'faces' : {'$in' : [photoid]}})
        if not user:
            return None

        return User(user['_id'], user['name'])

    def get_collection(self, name) -> MongoClient:
        if name in self.__collection:
            return self.__collection[name]

        client = MongoClient(self.__host_uri)
        self.__collection[name] = client[self.DATABASE_NAME][name]

        return self.__collection[name]