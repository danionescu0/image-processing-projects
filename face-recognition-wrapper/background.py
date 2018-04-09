import argparse

import cv2
import imutils
from image.FaceFileNamesProvider import FaceFileNamesProvider
from image.FaceRecognition import FaceRecognition

import config
from FaceDetectNotifier import FaceDetectNotifier
from MqttConnection import MqttConnection
from UserRepository import UserRepository
from image.FrameProvider import FrameProvider

# configure argument parser
parser = argparse.ArgumentParser(description='Configuration')
parser.add_argument('--show-video', dest='video', action='store_true', help='shows images on desktop')
parser.set_defaults(feature=False)
args = parser.parse_args()

user_repository = UserRepository(config.mongodb_uri)
mqtt_connection = MqttConnection(config.mqtt['host'], config.mqtt['port'], config.mqtt['user'], config.mqtt['password'])
mqtt_connection.connect()
face_notifier = FaceDetectNotifier(mqtt_connection, user_repository)
frame_provider = FrameProvider(config.process_image_delay_ms)
frame_provider.start()
face_filenames = FaceFileNamesProvider().load('./faces/')
face_recognition = FaceRecognition()
face_recognition.load_faces(face_filenames)


while not frame_provider.received_stop():
    if not frame_provider.has_frame():
        continue
    frame = frame_provider.get_frame()
    # image is resised by with with some amount in px for better performance
    frame = imutils.resize(frame, width=config.resize_image_by_width)
    frame = imutils.rotate(frame, config.rotate_camera_by)
    faces = face_recognition.find(frame)
    if len(faces) > 0:
        face_notifier.notify(faces)
    if args.video:
        cv2.imshow('frame', frame)

frame_provider.stop()