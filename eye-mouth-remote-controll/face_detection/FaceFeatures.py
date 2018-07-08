import imutils
from imutils import face_utils
import numpy as np

from face_detection.FaceModel import FaceModel


class FaceFeatures:
    def __init__(self, detector, predictor, resize_image_by_width: int ) -> None:
        self.__detector = detector
        self.__predictor = predictor
        self.__resize_image_by_width = resize_image_by_width

    def get_face_model(self, image) -> FaceModel:
        _, original_width = image.shape[:2]
        image = imutils.resize(image, width=self.__resize_image_by_width)
        scale_percent_from_resized = int((original_width - self.__resize_image_by_width) * 100 \
                                     / self.__resize_image_by_width)
        face_coordonates_rectangles = self.__detector(image, 1)
        if len(face_coordonates_rectangles) != 1:
            return FaceModel()
        face_rectangle = face_coordonates_rectangles[0]
        points = face_utils.shape_to_np(self.__predictor(image, face_rectangle))

        return FaceModel(self.__scale_face_model(points, scale_percent_from_resized))

    def __scale_face_model(self, points, percent: int):
        scaler = lambda point: (int(point[0] + point[0] * percent / 100), int(point[1] + point[1] * percent / 100))

        return np.array([scaler(point) for point in points])
