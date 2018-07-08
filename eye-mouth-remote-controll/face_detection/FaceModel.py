from enum import Enum


class FaceModel:
    class FeaturesMapping(Enum):
        LEFT_EYE = (36, 42)
        RIGHT_EYE = (42, 48)
        MOUTH = (48, 68)
        NOSE = (27, 36)

    def __init__(self, points = None) -> None:
        self.all_points = points

    def has_detection(self):
        return self.all_points is not None

    def get_left_eye(self):
        return self.__get(self.FeaturesMapping.LEFT_EYE.value)

    def get_right_eye(self):
        return self.__get(self.FeaturesMapping.RIGHT_EYE.value)

    def get_mouth(self):
        return self.__get(self.FeaturesMapping.MOUTH.value)

    def __get(self, part):
        return self.all_points[part[0]:part[1]]