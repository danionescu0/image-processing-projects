from MathUtils import MathUtils
from command.Coordonates import Coordonates


class EyeMouthCommands:
    def __init__(self, pupil_detector) -> None:
        self.__pupil_detector = pupil_detector

    def get(self, image, face_coordonates) -> Coordonates:
        pupil_center, eye_shape = self.__pupil_detector.find(image, face_coordonates)
        if pupil_center == False:
            return Coordonates()
        height, width, _ = eye_shape
        print(pupil_center, width)
        eyes_horizontal_angle = MathUtils.remap(pupil_center[0], 0, width, 0, 180)

        #@todo replace 10 with calculated value
        return Coordonates(eyes_horizontal_angle, 10)

    def update_pupil_black_threshold(self, value: int) -> None:
        self.__pupil_detector.update_pupil_black_threshold(value)
