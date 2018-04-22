import json

import tornado

from UserRepository import UserRepository


class UsersHandler(tornado.web.RequestHandler):
    LIMIT = 2

    def initialize(self, user_repo: UserRepository):
        self.__user_repo = user_repo

    def get(self):
        page = int(self.get_argument('page', 1, True))
        users = self.__user_repo.get_users(page * self.LIMIT, self.LIMIT)
        self.write(json.dumps(self.__get_formatted_users(users)))

    def __get_formatted_users(self, users: list) -> list:
        return [
            {
                'id': user.id,
                'name': user.name,
                'images': user.image_ids
             } for user in users]
