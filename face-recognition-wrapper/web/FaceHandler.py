import json
import os

import tornado

from UserRepository import UserRepository
from communication.MqttConnection import MqttConnection
from imageprocessing.FaceExtractor import FaceExtractor
from communication.FaceNotificator import FaceNotificator


class FaceHandler(tornado.web.RequestHandler):
    def initialize(self, user_repo: UserRepository, upload_path: str, face_extractor: FaceExtractor,
                   face_notificator: FaceNotificator):
        self.__user_repo = user_repo
        self.__upload_path = upload_path
        self.__face_extractor = face_extractor
        self.__face_notificator = face_notificator

    def post(self, face_id):
        fileinfo = self.request.files['photo'][0]
        filename = fileinfo['filename']
        user_id = self.get_argument('user_id', None, True)
        try:
            full_path = os.path.join(self.__upload_path, filename)
            with open(full_path, 'wb') as fh:
                fh.write(fileinfo['body'])
                valid = self.__face_extractor.is_valid(full_path)
                if valid['status'] is False:
                    self.set_status(500)
                    self.write(json.dumps(valid))
                else:
                    self.__add_face(full_path, face_id, user_id)

        except IOError as e:
            print("Failed to write file due to IOError %s", str(e))

    def __add_face(self, full_path: str, face_id: str, user_id: str):
        face_file_path = self.__face_extractor.process(full_path, face_id)
        self.__user_repo.add_face(face_id, user_id)
        self.__face_notificator.notify_added(user_id, face_id, face_file_path)