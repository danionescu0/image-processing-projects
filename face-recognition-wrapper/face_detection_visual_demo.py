import cv2
import imutils
import numpy


# define configuration
camera_width = 600
camera_height = 400
rotate_angle = 180
min_contour_area_for_motion_detection = 1000

# initialize camera video stream
capture = cv2.VideoCapture(0)
# set width and height
capture.set(3, camera_width)
capture.set(4, camera_height)

# initialize opencv BackgroundSubtractorMOG2
background_substractor = cv2.createBackgroundSubtractorMOG2(history=2)


# main loop, used to read frame by frame process the images until "q" is pressed
while not cv2.waitKey(30) & 0xFF == ord('q'):
    # read image from camera stream
    ret, frame = capture.read()
    # rotate image
    frame = imutils.rotate(frame, rotate_angle)
    # show frame
    cv2.imshow('original', frame)
    # apply background substraction from opencv
    fgmask = background_substractor.apply(frame)
    # use thresholding to split frame in motion and non motion if intensity is above 40
    thresh = cv2.threshold(fgmask, 40, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=3)
    # find contours of all objects
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not len(contours[1]):
        continue
    contours = [contour for contour in contours[1] if cv2.contourArea(contour) > min_contour_area_for_motion_detection]
    if len(contours) == 0:
        continue
    boxes = [cv2.boundingRect(countour) for countour in contours]
    x1, x2, y1, y2 = 5000, 5000, 5000, 5000
    for countour in contours:
        (x, y, w, h) = cv2.boundingRect(countour)
        x1 = min(x, x1)
        y1 = min(y, y1)
        x2 = min(x + w, x2)
        y2 = min(y + h, y2)
    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0))
    cv2.imshow('motion', frame)

# stop camera stream
capture.release()