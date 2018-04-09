import tornado

from UserRepository import UserRepository


class UserHandler(tornado.web.RequestHandler):
    def initialize(self, user_repo: UserRepository):
        self.__user_repo = user_repo

    def post(self, user_id):
        # data = json.loads(self.request.body.decode("utf-8"))
        print(user_id)
        self.set_status(200)