import argparse

import tornado.ioloop
import tornado.web

import config
from UserRepository import UserRepository
from communication.MqttConnection import MqttConnection
from communication.FaceNotificator import FaceNotificator

from imageprocessing.FaceExtractor import FaceExtractor
from web.FaceHandler import FaceHandler
from web.UserHandler import UserHandler


user_repo = UserRepository(config.mongodb_uri)
face_extractor = FaceExtractor('./faces/')
mqtt_connection = MqttConnection(config.mqtt['host'], config.mqtt['port'], config.mqtt['user'], config.mqtt['password'])
mqtt_connection.connect()
face_notificator = FaceNotificator(mqtt_connection)


def make_app():
    return tornado.web.Application([
        (r"/user/(\w*)", UserHandler, dict(user_repo=user_repo)),
        (r"/face/(\w*)", FaceHandler,
                 dict(
                     user_repo=user_repo,
                      upload_path='./temp',
                      face_extractor=face_extractor,
                     face_notificator=face_notificator
                 )
             )
    ])

parser = argparse.ArgumentParser(description='Configuration')
parser.add_argument('--port', dest='port', type=str, default=8080)
args = parser.parse_args()

if __name__ == "__main__":
    app = make_app()
    app.listen(args.port, '0.0.0.0')
    tornado.ioloop.IOLoop.current().start()