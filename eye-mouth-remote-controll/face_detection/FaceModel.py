from face_detection.FeaturesMapping import FeaturesMapping


class FaceModel:
    def __init__(self, points = None) -> None:
        self.__points = points

    def has_detection(self):
        return self.__points is not None

    def get_eye(self):
        return self.__points[FeaturesMapping.LEFT_EYE_COORDONATES.value[0]:FeaturesMapping.LEFT_EYE_COORDONATES.value[1]]
