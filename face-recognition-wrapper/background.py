import time
import argparse

import cv2
import imutils

import config
from FaceDetectNotifier import FaceDetectNotifier
from UserRepository import UserRepository
from communication.MqttConnection import MqttConnection
from communication.FaceNotificator import FaceNotificator
from communication.NotificationListener import NotificationListener
from communication.Notification import Notification
from imageprocessing.FaceFileNamesProvider import FaceFileNamesProvider
from imageprocessing.FaceRecognition import FaceRecognition
from imageprocessing.FrameProvider import FrameProvider
from imageprocessing.ImageEncoder import ImageEncoder
from imageprocessing.FaceRecognitionProcessWrapper import FaceRecognitionProcessWrapper


# configure argument parser
parser = argparse.ArgumentParser(description='Configuration')
parser.add_argument('--show-video', dest='video', action='store_true', help='shows video on desktop')
parser.set_defaults(feature=False)
args = parser.parse_args()

#configure objects with dependencies
image_encoder = ImageEncoder('./temp/')
user_repository = UserRepository(config.mongodb_uri)
mqtt_connection = MqttConnection(config.mqtt['host'], config.mqtt['port'], config.mqtt['user'], config.mqtt['password'])
mqtt_connection.connect()
face_notificator = FaceNotificator(mqtt_connection)
notification_listener = NotificationListener(mqtt_connection)

face_notifier = FaceDetectNotifier(face_notificator, user_repository)
frame_provider = FrameProvider(config.process_image_delay_ms)
frame_provider.start()
face_filenames = FaceFileNamesProvider().load('./faces/')
face_recognition = FaceRecognition()
face_recognition.load_faces(face_filenames)

face_recognition_process_wrapper = FaceRecognitionProcessWrapper(
    face_recognition, config.frame_processing_threads * 3, config.frame_processing_threads)
face_recognition_process_wrapper.start()


def do_load_face(user_id: str, face_id: str, file_path: str):
    face_recognition.load_face(file_path)

notification_listener.listen(do_load_face, Notification.FACE_PROCESSED.value)

while not frame_provider.received_stop():
    if not frame_provider.has_frame():
        continue
    frame = frame_provider.get_frame()
    # imageprocessing is resised by with with some amount in px for better performance
    frame = imutils.resize(frame, width=config.resize_image_by_width)
    frame = imutils.rotate(frame, config.rotate_camera_by)

    if args.video:
        cv2.imshow('frame', frame)
    face_recognition_process_wrapper.put_image(frame)
    result = face_recognition_process_wrapper.get_result()
    if result is None:
        continue
    image, faces = result
    if len(faces) > 0:
        face_notifier.notify(faces, image_encoder.encode(image))


frame_provider.stop()