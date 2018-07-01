import time
import argparse

from imutils import face_utils
import imutils
import dlib
import cv2

import config
from PupilDetector import PupilDetector
from robots.MqttConnection import MqttConnection
from robots.RobotSerialCommandsConverter import RobotSerialCommandsConverter
from command.EyeMouthCommands import EyeMouthCommands


argparse = argparse.ArgumentParser()
argparse.add_argument("-p", "--face-shape-predictor", required=True, dest="shape_predictor",
                      help="path to facial landmark predictor")
argparse.add_argument("-v", "--video-input", required=True, dest="video_input",
                      help="path to video input ex: /dev/video0")
args = vars(argparse.parse_args())

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

pupil_detector = PupilDetector(config.pupil_black_level)
draw_image_font = cv2.FONT_HERSHEY_SIMPLEX
camera_device = cv2.VideoCapture(args['video_input'])
mqtt_connection = MqttConnection(config.mqtt['host'], config.mqtt['port'], config.mqtt['user'], config.mqtt['password'])
eye_mouth_commands = EyeMouthCommands(pupil_detector)
robot_serial_command_converter = RobotSerialCommandsConverter()


while not cv2.waitKey(30) & 0xFF == ord('q'):
    ret, image = camera_device.read()
    image = imutils.resize(image, width=config.resize_image_by_width)
    image = imutils.rotate(image, config.rotate_camera_by)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_coordonates_rectangles = detector(gray, 1)
    if len(face_coordonates_rectangles) != 1:
        cv2.putText(image, "No face", (20, 20), draw_image_font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.imshow("Original", image)
        continue
    cv2.imshow("Original", image)
    cv2.createTrackbar('Pupil black value 0-255', 'Original', config.pupil_black_level, 255,
                       eye_mouth_commands.update_black_threshold)

    face_rectangle = face_coordonates_rectangles[0]
    face_coordonates = face_utils.shape_to_np(predictor(gray, face_rectangle))
    coordonates = eye_mouth_commands.get(image, face_coordonates)
    print(coordonates)

camera_device.release()
