from calibration.CalibratedModel import CalibratedModel
from face_detection.PupilDetector import PupilDetector
from face_detection.FaceModel import FaceModel
from face_detection.ShapeAnalizer import ShapeAnalizer


class Calibrator:
    SUPPORTED_CALIBRATIONS = {
        81: 'max_left_pupil',
        83: 'min_left_pupil',
        84: 'mounth_closed',
        82: 'mouth_opened'
    }

    def __init__(self, pupil_detector: PupilDetector, shape_analizer: ShapeAnalizer) -> None:
        self.__pupil_detector = pupil_detector
        self.__shape_analizer = shape_analizer
        self.calibrated_model = CalibratedModel()

    def supports_calibration(self, key: int) -> bool:
        return key in self.SUPPORTED_CALIBRATIONS

    def calibrate(self, key: int, image, face_model: FaceModel):
        calibration_type = self.SUPPORTED_CALIBRATIONS[key]
        if calibration_type in ['max_left_pupil', 'min_left_pupil']:
            self.__calibrate_eyes(calibration_type, image, face_model)
        elif calibration_type in ['mounth_closed', 'mouth_opened']:
            self.__calibrate_mouth(calibration_type, face_model)

    def __calibrate_eyes(self, which: str, image, face_model: FaceModel):
        center, image_shape = self.__pupil_detector.find(image, face_model)
        if center is False:
            return
        if which == 'max_left_pupil':
            self.calibrated_model.eye_max_left = center[0]
        elif which == 'min_left_pupil':
            self.calibrated_model.eye_max_right = center[0]

    def __calibrate_mouth(self, which: str, face_model: FaceModel):
        mouth_height = self.__shape_analizer.get_height(face_model.get_mouth())
        if which == 'mounth_closed':
            self.calibrated_model.mouth_closed_height = mouth_height
        elif which == 'mouth_opened':
            self.calibrated_model.mouth_opened_height = mouth_height