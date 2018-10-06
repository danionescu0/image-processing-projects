import argparse

import cv2
import imutils
import numpy

import config
from UserRepository import UserRepository
from FrameProvider import FrameProvider
from communication.MqttConnection import MqttConnection
from communication.FaceNotificator import FaceNotificator
from communication.NotificationListener import NotificationListener
from communication.Notification import Notification
from imageprocessing.FaceFileNamesProvider import FaceFileNamesProvider
from imageprocessing.FaceRecognition import FaceRecognition
from imageprocessing.ImageEncoder import ImageEncoder
from imageprocessing.FaceRecognitionProcessWrapper import FaceRecognitionProcessWrapper
from imageprocessing.ImageDebug import ImageDebug
from imageprocessing.MotionDetector import MotionDetector
from imageprocessing.CoordonatesScaler import CoordonatesScaler


# configure argument parser
parser = argparse.ArgumentParser(description='Configuration')
parser.add_argument('--show-video', dest='video', action='store_true', help='Shows video on GUI')
parser.add_argument('-cd', '--camera_device', dest='camera', type=int)
parser.add_argument('-m', '--use_motion', dest='motion', action='store_true')
parser.set_defaults(feature=False)
args = parser.parse_args()

# initialize the image encoder, this is responsable for encoding an image as string to be sent over MQTT
image_encoder = ImageEncoder()

# user repository responsable for persisting user information in the database
user_repository = UserRepository(config.mongodb_uri)

# MQTT connection, this is used to broadcast found faces
mqtt_connection = MqttConnection(config.mqtt['host'], config.mqtt['port'],
                                 config.mqtt['user'], config.mqtt['password'])
mqtt_connection.connect()

# this object uses the MqttConnection and user repository to actually broadcast the faces
face_notificator = FaceNotificator(mqtt_connection, user_repository, config.faces_path)

# listens to add face / delete face events and actually ads them or deletes them on disk and on the database
notification_listener = NotificationListener(mqtt_connection)


# configure the video stream
frame_provider = FrameProvider(args.camera, config.image, (1600, 1200))

scaler = CoordonatesScaler()

# configure motion detector
motion_detector = MotionDetector(scaler, config.image['resize_image_by_width'], 1000)
motion_detector.configure()

# load the files on disk containing the faces and create the face recognition object
filepaths = FaceFileNamesProvider().load(config.faces_path)
face_recognition = FaceRecognition(scaler, config.image['resize_image_by_width'])
face_recognition.load_faces(filepaths)

# configure the face recognition process wrapper
face_recognition_process_wrapper = FaceRecognitionProcessWrapper(face_recognition, config.frame_processing_threads)
face_recognition_process_wrapper.start()

# initialize the image debug, this will draw a circle and the face id on the image for debugging purposes
image_debug = ImageDebug((0, 255, 255), 2)

# load new face in face detection system without restarting
notification_listener.listen(Notification.FACE_ADDED.value,
                             lambda user_id, face_id, file_path: face_recognition.load_face(file_path))

# delete face from face detection system
notification_listener.listen(Notification.FACE_DELETED.value, lambda face_id: face_recognition.delete_face(face_id))

frame_provider.start()


def show_debug_image(name: str, image):
    if args.video and type(image) is numpy.ndarray:
        image = imutils.resize(image, width=600)
        cv2.imshow(name, image)

# the main loop, process frame by frame resises and rotates the frames if needed
# this will call the face recognition mechanism and notify if faces are found
while not cv2.waitKey(30) & 0xFF == ord('q'):
    frame_provider.update_frame()
    frame = frame_provider.get_last_frame()
    show_debug_image('frame', frame)
    # if the script ran with --use_motion first detect motion in the frame
    if args.motion:
        detected_motion_box = motion_detector.get_motion_box(frame)
        if detected_motion_box is not None:
            face_recognition_process_wrapper.put_image(detected_motion_box)
    else:
        face_recognition_process_wrapper.put_image(frame)

    # get asyncronious result
    image_with_detection, faces = face_recognition_process_wrapper.get_result()
    # when a detection has been found
    if image_with_detection is not None and len(faces) > 0:
        # draw circles around faces and write identifiers near them
        image_with_detection = image_debug.enhance_with_debug(image_with_detection, faces)
        show_debug_image('last_capture', image_with_detection)
        # broadcast over MQTT
        face_notificator.notify_found(faces, image_encoder.encode_numpy_image(image_with_detection))

frame_provider.stop()