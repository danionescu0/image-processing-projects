from face_detection.FaceModel import FaceModel
from face_detection.ShapeAnalizer import ShapeAnalizer


class FaceModelValidator:
    __MAX_PERCENT_DIFFERENCE_IN_EYES_WIDTH = 7

    def __init__(self, shape_analizer: ShapeAnalizer, mandatory_face_height_percent: int) -> None:
        self.__shape_analizer = shape_analizer
        self.__mandatory_face_height_percent = mandatory_face_height_percent

    def is_valid(self, image, model: FaceModel) -> bool:
        if not model.has_detection() or not self.__is_face_proportion_right(image, model)\
                or not self.__are_eyes_width_equal(model):
            return False

        return True

    def __is_face_proportion_right(self, image, model: FaceModel) -> bool:
        face_height = self.__shape_analizer.get_height(model.all_points)
        image_height, _ = image.shape[:2]
        minimum_accepted_height = int(image_height * self.__mandatory_face_height_percent / 100)

        return face_height >= minimum_accepted_height

    def __are_eyes_width_equal(self, model: FaceModel) -> bool:
        left_eye_width = self.__shape_analizer.get_width(model.get_left_eye())
        right_eye_width = self.__shape_analizer.get_width(model.get_right_eye())
        if left_eye_width - right_eye_width == 0:
            return True
        percent_difference_in_width =  int((
                abs(left_eye_width - right_eye_width) /
                max(left_eye_width, right_eye_width)
            ) * 100)

        return percent_difference_in_width <= self.__MAX_PERCENT_DIFFERENCE_IN_EYES_WIDTH