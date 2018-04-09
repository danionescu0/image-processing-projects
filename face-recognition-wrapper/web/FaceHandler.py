import os

import tornado

from UserRepository import UserRepository


class FaceHandler(tornado.web.RequestHandler):
    def initialize(self, user_repo: UserRepository, upload_path: str):
        self.__user_repo = user_repo
        self.__upload_path = upload_path

    def post(self, user_id):
        fileinfo = self.request.files['photo'][0]
        filename = fileinfo['filename']
        try:
            with open(os.path.join(self.__upload_path, filename), 'wb') as fh:
                fh.write(fileinfo['body'])
        except IOError as e:
            print("Failed to write file due to IOError %s", str(e))