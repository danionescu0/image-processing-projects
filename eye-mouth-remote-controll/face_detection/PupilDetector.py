from typing import Tuple

import cv2
import numpy as np

from face_detection.FaceModel import FaceModel


class PupilDetector:
    __BLACK_THRESHOLD = (10, 150)

    def find(self, image, face_model: FaceModel) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        cropped_eye = self.__crop_eye(image, face_model)
        gray = cv2.cvtColor(cropped_eye, cv2.COLOR_BGR2GRAY)
        contours, thresh = self.find_pupil_using_adaptive_threshold(gray)
        cv2.imshow("Eye", cropped_eye)
        cv2.imshow("Pupil", thresh)
        if len(contours) == 0:
            return (False, cropped_eye.shape)
        largest_contour = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)
        M = cv2.moments(largest_contour)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        return (center, cropped_eye.shape)

    def find_pupil_using_adaptive_threshold(self, image):
        for black_threshold in range(self.__BLACK_THRESHOLD[0], self.__BLACK_THRESHOLD[1], 3):
            thresh = cv2.threshold(image, black_threshold, 255, cv2.THRESH_BINARY_INV)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
            contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)[-2]
            if len(contours):
                return contours, thresh

        return contours, thresh

    def __crop_eye(self, image, face_model: FaceModel):
        eye = face_model.get_left_eye()
        mask = np.full(image.shape, 255, dtype=np.uint8)
        channel_count = image.shape[2]
        ignore_mask_color = (0,) * channel_count
        cv2.fillPoly(mask, np.array([eye]), ignore_mask_color)
        eye_mask = cv2.bitwise_or(image, mask)
        (x, y, w, h) = cv2.boundingRect(np.array([eye]))
        cropped_eye = eye_mask[y:y + h, x:x + w]

        return cropped_eye