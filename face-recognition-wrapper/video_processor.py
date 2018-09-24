import argparse

import cv2
from imutils.video import VideoStream

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
from imageprocessing.FaceDetector import FaceDetector
from imageprocessing.ImageDebug import ImageDebug


# configure argument parser
parser = argparse.ArgumentParser(description='Configuration')
parser.add_argument('--show-video', dest='video', action='store_true', help='Shows video on GUI')
parser.add_argument('-cd', '--camera_device', dest='camera', type=int)
parser.set_defaults(feature=False)
args = parser.parse_args()

# initialize the image encoder, this is responsable for encoding an image as string to be sent over MQTT
image_encoder = ImageEncoder()

# user repository responsable for persisting user information in the database
user_repository = UserRepository(config.mongodb_uri)

# mqtt connection for communication found faces
mqtt_connection = MqttConnection(config.mqtt['host'], config.mqtt['port'],
                                 config.mqtt['user'], config.mqtt['password'])
mqtt_connection.connect()

face_notificator = FaceNotificator(mqtt_connection, user_repository, config.faces_path)
notification_listener = NotificationListener(mqtt_connection)


# configure the video stream
video_stream = VideoStream(args.camera).start()
frame_provider = FrameProvider(video_stream, config.image)

# load the files on disk containing the faces and create the face recognition object
filepaths = FaceFileNamesProvider().load(config.faces_path)
face_detector = FaceDetector(
    config.resources_path + 'deploy.prototxt.txt',
    config.resources_path + 'res10_300x300_ssd_iter_140000.caffemodel',
    0.5)
face_detector.configure()
face_recognition = FaceRecognition(face_detector)
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

# the main loop, process frame by frame resises and rotates the frames if needed
# this will call the face recognition mechanism and notify if faces are found
while not cv2.waitKey(30) & 0xFF == ord('q'):
    frame = frame_provider.read()
    face_recognition_process_wrapper.put_image(frame)
    image_with_detection, faces = face_recognition_process_wrapper.get_result()
    # when a detection has been found async using the process wrapper
    # notify listeners using MQTT
    if image_with_detection is not None and len(faces) > 0:
        image_with_detection = image_debug.enhance_with_debug(image_with_detection, faces)
        face_notificator.notify_found(faces, image_encoder.encode_numpy_image(image_with_detection))
        if args.video:
            cv2.imshow('last_capture', image_with_detection)
    if args.video:
        cv2.imshow('frame', frame)

frame_provider.stop()