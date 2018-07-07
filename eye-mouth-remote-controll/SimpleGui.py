from typing import Tuple

import cv2


class SimpleGui:
    def __init__(self, screen: Tuple[int, int]):
        self.__screen = screen

    def create_windows(self):
        full_image_size = int(min(self.__screen[0], self.__screen[1]) / 2)
        eye_image_size = int(full_image_size / 3)
        self.__create_window('Original', (50, 50), (full_image_size, full_image_size))
        self.__create_window('Eye', (full_image_size + 100, 50), (eye_image_size, eye_image_size))
        self.__create_window('Pupil', (full_image_size + 100, 100 + eye_image_size), (eye_image_size, eye_image_size))

    def __create_window(self, name: str, position: tuple, size: tuple):
        cv2.namedWindow(name, cv2.WINDOW_NORMAL)
        cv2.moveWindow(name, position[0], position[1])
        cv2.resizeWindow(name, size[0], size[1])