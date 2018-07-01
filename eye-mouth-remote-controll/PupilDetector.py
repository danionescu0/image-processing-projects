from typing import Tuple

import cv2
import numpy as np


class PupilDetector:
    __LEFT_EYE_COORDONATES = (36, 42)

    def __init__(self, black_threshold: int) -> None:
        self.__black_threshold = black_threshold

    def find(self, image, face_coordonates) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        cropped_eye = self.__crop_eye(image, face_coordonates)
        cv2.imshow("Eye", cropped_eye)

        gray = cv2.cvtColor(cropped_eye, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, self.__black_threshold, 255, cv2.THRESH_BINARY_INV)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        cv2.imshow("Pupil", thresh)

        contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]

        if len(contours) == 0:
            return (False, cropped_eye.shape)
        largest_contour = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)
        M = cv2.moments(largest_contour)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        return (center, cropped_eye.shape)

    def update_black_threshold(self, value: int) -> None:
        self.__black_threshold = value

    def __crop_eye(self, image, face_coordonates):
        eye = face_coordonates[self.__LEFT_EYE_COORDONATES[0]:self.__LEFT_EYE_COORDONATES[1]]
        mask = np.full(image.shape, 255, dtype=np.uint8)
        channel_count = image.shape[2]
        ignore_mask_color = (0,) * channel_count
        cv2.fillPoly(mask, np.array([eye]), ignore_mask_color)
        eye_mask = cv2.bitwise_or(image, mask)
        (x, y, w, h) = cv2.boundingRect(np.array([eye]))
        cropped_eye = eye_mask[y:y + h, x:x + w]

        return cropped_eye