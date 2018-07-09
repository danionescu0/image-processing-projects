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
from face_detection.ShapeAnalizer import ShapeAnalizer
from face_detection.FaceModelValidator import FaceModelValidator
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

timer = Timer()
pupil_detector = PupilDetector()
shape_analizer = ShapeAnalizer()
dlib_face_detector = dlib.get_frontal_face_detector()
dlib_shape_predictor = dlib.shape_predictor(args["shape_predictor"])
face_features = FaceFeatures(dlib_face_detector, dlib_shape_predictor, config.resize_image_by_width)
frame_provider = FrameProviderProcessWrapper(args['video_input'], config.rotate_camera_by)
face_model_validator = FaceModelValidator(shape_analizer, 65)
eye_mouth_commands = EyeMouthCommands(pupil_detector, shape_analizer)
robot_serial_command_converter = RobotSerialCommandsConverter()
calibrator = Calibrator(pupil_detector, shape_analizer)
mqtt_connection = MqttConnection(config.mqtt['host'], config.mqtt['port'], config.mqtt['user'], config.mqtt['password'])
simple_gui = SimpleGui(config.screen)

frame_provider.start()
mqtt_connection.connect()
simple_gui.initialize()
last_valid_key_press = None

while True:
    key_pressed = cv2.waitKey(1) & 0xFF
    if calibrator.supports_calibration(key_pressed):
        last_valid_key_press = key_pressed
    original_image = frame_provider.get_last_frame()
    if original_image is None:
        continue
    simple_gui.image = imutils.resize(original_image, width=config.resize_image_by_width)
    face_model = face_features.get_face_model(original_image)
    if not calibrator.calibrated_model.is_calibrated():
        simple_gui.write_text_on_main("No calibration", 2)
    if not face_model_validator.is_valid(original_image, face_model):
        simple_gui.write_text_on_main("No face", 1)
        simple_gui.display_main_img()
        continue
    simple_gui.display_main_img()

    if calibrator.supports_calibration(last_valid_key_press):
        calibrator.calibrate(last_valid_key_press, original_image, face_model)
        eye_mouth_commands.calibrated_model = calibrator.calibrated_model
        last_valid_key_press = None
        print(calibrator.calibrated_model)
    coordonates = eye_mouth_commands.get(original_image, face_model)
    if coordonates.has_detection():
        command = robot_serial_command_converter.get_from_coordonates(coordonates)
        simple_gui.draw_controls(coordonates.eyes_horizontal_angle, coordonates.mouth_vertical_percent)
        print(coordonates, command)
        mqtt_connection.send_movement_command(command)
