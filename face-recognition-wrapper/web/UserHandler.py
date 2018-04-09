import tornado

from UserRepository import UserRepository
from model.User import User


class UserHandler(tornado.web.RequestHandler):
    def initialize(self, user_repo: UserRepository):
        self.__user_repo = user_repo

    def post(self, user_id):
        name = self.get_argument('name', None, True)
        if name is None:
            raise Exception("Please provide name")
        self.__user_repo.add_user(User(user_id, name))