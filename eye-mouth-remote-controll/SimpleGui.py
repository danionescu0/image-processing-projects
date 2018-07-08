from typing import Tuple

import imutils
import cv2

from MathUtils import MathUtils


class SimpleGui:
    def __init__(self, screen: Tuple[int, int]):
        self.__screen = screen
        self.__wheel_path = './steering_wheel.png'
        self.__wheel_img = None
        self.__draw_image_font = cv2.FONT_HERSHEY_SIMPLEX

    def initialize(self):
        full_image_size = int(min(self.__screen[0], self.__screen[1]) / 2)
        eye_image_size = int(full_image_size / 3)
        self.__create_window('Original', (50, 50), (full_image_size, full_image_size))
        self.__create_window('Eye', (full_image_size + 100, 50), (eye_image_size, eye_image_size))
        self.__create_window('Pupil', (full_image_size + 100, 100 + eye_image_size), (eye_image_size, eye_image_size))
        self.__create_window('Wheel', (full_image_size + 100, 400 + eye_image_size), (eye_image_size, eye_image_size))
        self.__wheel_img = cv2.imread(self.__wheel_path)
        cv2.imshow('Wheel', self.__wheel_img)

    def __create_window(self, name: str, position: tuple, size: tuple):
        cv2.namedWindow(name, cv2.WINDOW_NORMAL)
        cv2.moveWindow(name, position[0], position[1])
        cv2.resizeWindow(name, size[0], size[1])

    def write_text(self, image, text: str, row: int):
        cv2.putText(image, text, (20, row * 30), self.__draw_image_font, 0.8, (255, 255, 255), 1, cv2.LINE_AA)

        return image

    def rotate_wheel(self, angle: int):
        image_angle = angle
        if angle >=0 and angle <= 90:
            image_angle = MathUtils.remap(angle, 0, 90, 90, 0)
        elif angle > 90 and angle <= 180:
            image_angle = MathUtils.remap(angle, 90, 180, 0, -90)
        image = imutils.rotate(self.__wheel_img, image_angle)
        cv2.imshow('Wheel', image)