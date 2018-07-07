import argparse

import cv2
import dlib
import imutils

import config
from SimpleGui import SimpleGui
from calibration.Calibrator import Calibrator
from command.EyeMouthCommands import EyeMouthCommands
from face_detection.PupilDetector import PupilDetector
from face_detection.FaceFeatures import FaceFeatures
from robot_speed_angle.MqttConnection import MqttConnection
from robot_speed_angle.RobotSerialCommandsConverter import RobotSerialCommandsConverter
from video.FrameProviderProcessWrapper import FrameProviderProcessWrapper
from Timer import Timer


argparse = argparse.ArgumentParser()
argparse.add_argument("-p", "--face-shape-predictor", required=True, dest="shape_predictor",
                      help="path to facial landmark predictor")
argparse.add_argument("-v", "--video-input", required=True, dest="video_input",
                      help="path to video input ex: /dev/video0")
args = vars(argparse.parse_args())

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])
face_features = FaceFeatures(detector, predictor)
frame_provider = FrameProviderProcessWrapper(args['video_input'])
pupil_detector = PupilDetector()
draw_image_font = cv2.FONT_HERSHEY_SIMPLEX
mqtt_connection = MqttConnection(config.mqtt['host'], config.mqtt['port'], config.mqtt['user'], config.mqtt['password'])
simple_gui = SimpleGui(config.screen)
eye_mouth_commands = EyeMouthCommands(pupil_detector, simple_gui)
robot_serial_command_converter = RobotSerialCommandsConverter()
calibrator = Calibrator(pupil_detector)
timer = Timer()

frame_provider.start()
mqtt_connection.connect()
simple_gui.initialize()


while True:
    key_pressed = cv2.waitKey(1) & 0xFF
    image = frame_provider.get_last_frame()
    if image is None:
        continue
    image = imutils.resize(image, width=config.resize_image_by_width)
    image = imutils.rotate(image, config.rotate_camera_by)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_model = face_features.get_face_model(gray_image)
    if not face_model.has_detection():
        cv2.putText(image, "No face", (20, 20), draw_image_font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.imshow("Original", image)
        continue
    cv2.imshow("Original", image)

    if calibrator.supports_calibration(key_pressed):
        calibrator.calibrate(key_pressed, image, face_model)
        eye_mouth_commands.calibrated_model = calibrator.calibrated_model
        print(calibrator.calibrated_model)
    coordonates = eye_mouth_commands.get(image, face_model)
    if coordonates.has_detection():
        command = robot_serial_command_converter.get_from_coordonates(coordonates)
        print(coordonates, command)
        mqtt_connection.send_movement_command(command)