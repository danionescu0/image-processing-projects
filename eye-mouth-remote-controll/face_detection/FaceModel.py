from enum import Enum


class FaceModel:
    class FeaturesMapping(Enum):
        LEFT_EYE = (36, 42)
        MOUTH = (48, 68)
        NOSE = (27, 36)

    def __init__(self, points = None) -> None:
        self.__points = points

    def has_detection(self):
        return self.__points is not None

    def get_eye(self):
        return self.__get(self.FeaturesMapping.LEFT_EYE.value)

    def get_mouth(self):
        return self.__get(self.FeaturesMapping.MOUTH.value)

    def get_nose(self):
        return self.__get(self.FeaturesMapping.NOSE.value)

    def __get(self, part):
        return self.__points[part[0]:part[1]]