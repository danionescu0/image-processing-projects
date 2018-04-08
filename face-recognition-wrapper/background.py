import time
import argparse
import sys

import cv2
import imutils

import config
from FrameProvider import FrameProvider
from FaceRecognition import FaceRecognition
from FaceFileNamesProvider import FaceFileNamesProvider



frame_provider = FrameProvider(config.process_image_delay_ms)
frame_provider.start()
face_filenames = FaceFileNamesProvider().load('./faces/')
face_recognition = FaceRecognition()
face_recognition.load_faces(face_filenames)
print (face_filenames)

while not frame_provider.received_stop():
    if not frame_provider.has_frame():
        continue
    frame = frame_provider.get_frame()
    # image is resised by with with some amount in px for better performance
    frame = imutils.resize(frame, width=config.resize_image_by_width)
    frame = imutils.rotate(frame, config.rotate_camera_degrees)
    print(face_recognition.find(frame))
    # if args.video:
    cv2.imshow('frame', frame)

frame_provider.stop()