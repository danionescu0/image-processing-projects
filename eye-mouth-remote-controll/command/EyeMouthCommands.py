from MathUtils import MathUtils
from command.Coordonates import Coordonates
from calibration.CalibratedModel import CalibratedModel
from face_detection.FaceModel import FaceModel


class EyeMouthCommands:
    def __init__(self, pupil_detector) -> None:
        self.__pupil_detector = pupil_detector
        self._calibrated_model = None

    def get(self, image, face_model: FaceModel) -> Coordonates:
        pupil_center, eye_shape = self.__pupil_detector.find(image, face_model)
        if pupil_center == False:
            return Coordonates()
        height, width, _ = eye_shape
        from_low, from_high = self.__get_eyes_from_values(width)

        print(self.calibrated_model, pupil_center[0], from_low, from_high)
        eyes_horizontal_angle = MathUtils.remap(pupil_center[0], from_low, from_high, 0, 180)

        #@todo replace 10 with calculated value
        return Coordonates(eyes_horizontal_angle, 10)

    def __get_eyes_from_values(self, width: int):
        if self.calibrated_model is not None and self.calibrated_model.has_eyes_calibration():
            from_low = self.calibrated_model.eye_max_left
            from_high = self.calibrated_model.eye_max_right
            return from_low, from_high

        return 0, width

    def update_pupil_black_threshold(self, value: int) -> None:
        self.__pupil_detector.update_black_threshold(value)

    @property
    def calibrated_model(self):
        return self._calibrated_model

    @calibrated_model.setter
    def calibrated_model(self, value: CalibratedModel):
        self._calibrated_model = value