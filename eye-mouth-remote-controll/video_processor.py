import time
import argparse

from imutils import face_utils
import numpy as np
import imutils
import dlib
import cv2

from PupilCoordonates import ColoredObjectDetector

argparse = argparse.ArgumentParser()
argparse.add_argument("-p", "--face-shape-predictor", required=True, dest="shape_predictor",
                      help="path to facial landmark predictor")
argparse.add_argument("-v", "--video-input", required=True, dest="video_input",
                      help="path to video input ex: /dev/video0")
args = vars(argparse.parse_args())

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

colored_object_detector = ColoredObjectDetector()
left_eye = (36, 42)
camera_device = cv2.VideoCapture(args['video_input'])

while not cv2.waitKey(30) & 0xFF == ord('q'):
    ret, image = camera_device.read()
    time1 = time.time()
    image = imutils.resize(image, width=800)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 1)
    cv2.imshow("Original", image)

    for (i, rect) in enumerate(rects):
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        eye = shape[left_eye[0]:left_eye[1]]
        mask = np.full(image.shape, 255, dtype=np.uint8)
        channel_count = image.shape[2]
        ignore_mask_color = (0,) * channel_count
        cv2.fillPoly(mask, np.array([eye]), ignore_mask_color)
        eye_mask = cv2.bitwise_or(image, mask)
        (x, y, w, h) = cv2.boundingRect(np.array([eye]))
        cropped_eye = eye_mask[y:y + h, x:x + w]

        center, radius = colored_object_detector.find_pupil(cropped_eye)
        if center is not False:
            cv2.circle(cropped_eye, center, radius, (0, 255, 255), 1)

        cv2.imshow("Cropped eye", cropped_eye)

camera_device.release()
