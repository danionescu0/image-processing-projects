from imutils import face_utils

from face_detection.FaceModel import FaceModel


class FaceFeatures:
    def __init__(self, detector, predictor) -> None:
        self.__detector = detector
        self.__predictor = predictor

    def get_face_model(self, image) -> FaceModel:
        face_coordonates_rectangles = self.__detector(image, 1)
        if len(face_coordonates_rectangles) != 1:
            return FaceModel
        face_rectangle = face_coordonates_rectangles[0]

        return FaceModel(face_utils.shape_to_np(self.__predictor(image, face_rectangle)))

