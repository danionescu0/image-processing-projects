from typing import List

import cv2

from model.DetectedFace import DetectedFace


class ImageDebug:
    def __init__(self, color, line_width) -> None:
        self.__color = color
        self.__line_width = line_width
        self.__font = cv2.FONT_HERSHEY_SIMPLEX

    #draws a circle around the faces
    #wite the person names near the face
    def enhance_with_debug(self, image, faces: List[DetectedFace]):
        for face in faces:
            center = (face.right - int((face.right - face.left) / 2), face.top + int((face.bottom - face.top) / 2))
            radius = int((face.bottom - face.top + 0.3 * (face.bottom - face.top)) / 2)
            cv2.circle(image, center, radius, self.__color, self.__line_width)
            image_text = 'id: ' + face.id if face.id is not None else 'Unknown'
            text_coordonates = (face.left - 10, face.top - 10)
            cv2.putText(image, image_text, text_coordonates, self.__font, 2, (255, 255, 255), 3, cv2.LINE_AA)

        return image