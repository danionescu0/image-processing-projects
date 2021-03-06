import argparse

import tornado.ioloop
import tornado.web

import config
from UserRepository import UserRepository
from communication.MqttConnection import MqttConnection
from communication.FaceNotificator import FaceNotificator
from imageprocessing.FaceExtractor import FaceExtractor
from imageprocessing.ImageEncoder import ImageEncoder
from imageprocessing.FacePaths import FacePaths
from web.FaceHandler import FaceHandler
from web.UserHandler import UserHandler
from web.UsersHandler import UsersHandler


# configure objects instances
user_repo = UserRepository(config.mongodb_uri)
face_paths = FacePaths(config.faces_path)
face_extractor = FaceExtractor(face_paths)
mqtt_connection = MqttConnection(config.mqtt['host'], config.mqtt['port'], config.mqtt['user'], config.mqtt['password'])
mqtt_connection.connect()
face_notificator = FaceNotificator(mqtt_connection, user_repo, config.faces_path)
image_encoder = ImageEncoder()


# create tornado web app with UserHandler, UsersHandler and FaceHandler
def make_app():
    return tornado.web.Application([
        (r"/user/(\w*)", UserHandler,
                dict(
                    user_repo=user_repo)
                ),
        (r"/users", UsersHandler,
                dict(
                    user_repo=user_repo,
                    image_encoder=image_encoder,
                    face_paths=face_paths
                )),
        (r"/face/(\w*)", FaceHandler,
                 dict(
                     user_repo=user_repo,
                     upload_path=config.faces_path,
                     face_extractor=face_extractor,
                     face_paths=face_paths,
                     face_notificator=face_notificator
                 )
             )
    ])

# configure argument parser
parser = argparse.ArgumentParser(description='Configuration')
parser.add_argument('--port', dest='port', type=str, default=8080)
args = parser.parse_args()

# start webserver
if __name__ == "__main__":
    app = make_app()
    app.listen(args.port, '0.0.0.0')
    tornado.ioloop.IOLoop.current().start()