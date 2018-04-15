import time
import argparse

import cv2
import imutils

import config
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
face_notificator = FaceNotificator(mqtt_connection, user_repository, './faces/')
notification_listener = NotificationListener(mqtt_connection)

frame_provider = FrameProvider(config.process_image_delay_ms)
frame_provider.start()
face_filenames = FaceFileNamesProvider().load('./faces/')
face_recognition = FaceRecognition()
face_recognition.load_faces(face_filenames)

face_recognition_process_wrapper = FaceRecognitionProcessWrapper(
    face_recognition, config.frame_processing_threads * 3, config.frame_processing_threads)
face_recognition_process_wrapper.start()

# load new face in face detection system without restarting
notification_listener.listen(Notification.FACE_ADDED.value,
                             lambda user_id, face_id, file_path :face_recognition.load_face(file_path))

# delete face from face detection system
notification_listener.listen(Notification.FACE_DELETED.value, lambda face_id: face_recognition.delete_face(face_id))

# process frame by frame
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
        face_notificator.notify_found(faces, image_encoder.encode(image))


frame_provider.stop()