from MathUtils import MathUtils
from command.Coordonates import Coordonates
from calibration.CalibratedModel import CalibratedModel
from face_detection.FaceModel import FaceModel
from face_detection.PupilDetector import PupilDetector
from face_detection.ShapeAnalizer import ShapeAnalizer


class EyeMouthCommands:
    def __init__(self, pupil_detector: PupilDetector, shape_analizer: ShapeAnalizer) -> None:
        self.__pupil_detector = pupil_detector
        self.__shape_analizer = shape_analizer
        self._calibrated_model = CalibratedModel()

    def get(self, image, face_model: FaceModel) -> Coordonates:
        pupil_center, eye_shape = self.__pupil_detector.find(image, face_model)
        mouth_height = self.__shape_analizer.get_height(face_model.get_mouth())
        if not pupil_center or not self.calibrated_model.is_calibrated():
            return Coordonates()
        height, width, _ = eye_shape
        from_low, from_high = (self.calibrated_model.eye_max_left, self.calibrated_model.eye_max_right)
        pupil_center_width = int(MathUtils.constrain(pupil_center[0], (from_low, from_high)))
        eyes_horizontal_angle = MathUtils.remap(pupil_center_width, from_low, from_high, 0, 180)

        mouth_height = int(MathUtils.constrain(mouth_height,
                                               (self.calibrated_model.mouth_closed_height,
                                                self.calibrated_model.mouth_opened_height)))
        mouth_vertical_percent = MathUtils.remap(mouth_height, self.calibrated_model.mouth_closed_height,
                                                 self.calibrated_model.mouth_opened_height, 0, 100)

        return Coordonates(eyes_horizontal_angle, mouth_vertical_percent)

    @property
    def calibrated_model(self) -> CalibratedModel:
        return self._calibrated_model

    @calibrated_model.setter
    def calibrated_model(self, value: CalibratedModel):
        self._calibrated_model = value