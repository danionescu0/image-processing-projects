from typing import Optional
from typing import List

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
        self.__get_collection(self.COLLECTION_NAME)\
            .update_one({"_id": user.id}, update_data, True)

    def get_users(self, offset: int, limit: int) -> List[User]:
        raw_data = list(self.__get_collection(self.COLLECTION_NAME)\
            .find().skip(offset).limit(limit))
        users = []
        for user_data in raw_data:
            user = User(user_data['_id'], user_data['name'])
            user.image_ids = user_data['faces']
            users.append(user)

        return users

    def add_face(self, face_id: str, userid: str):
        update_data = {
            "$addToSet" : {
                "faces": face_id
            }
        }
        self.__get_collection(self.COLLECTION_NAME)\
            .update_one({"_id": userid}, update_data, True)

    def delete_face(self, face_id: str):
        update_data = {
            "$pull": {
                "faces": face_id
            }
        }
        self.__get_collection(self.COLLECTION_NAME)\
            .update_one({"faces": face_id}, update_data)

    def get_user(self, face_id: str) -> Optional[User]:
        if not face_id:
            return None
        user = self.__get_collection(self.COLLECTION_NAME)\
            .find_one({'faces' : {'$in' : [face_id]}})
        if not user:
            return None

        return User(user['_id'], user['name'])

    def __get_collection(self, name) -> MongoClient:
        if name in self.__collection:
            return self.__collection[name]

        client = MongoClient(self.__host_uri)
        self.__collection[name] = client[self.DATABASE_NAME][name]

        return self.__collection[name]