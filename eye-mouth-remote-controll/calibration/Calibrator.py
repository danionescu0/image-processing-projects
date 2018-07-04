from calibration.CalibratedModel import CalibratedModel
from PupilDetector import PupilDetector


class Calibrator:
    SUPPORTED_CALIBRATIONS = {
        81: 'max_left_pupil',
        83: 'min_left_pupil',
        84: 'mounth_closed',
        85: 'mouth_opened',
    }

    def __init__(self, pupil_detector: PupilDetector) -> None:
        self.__pupil_detector = pupil_detector
        self.calibrated_model = CalibratedModel()

    def supports_calibration(self, key: int) -> bool:
        return key in self.SUPPORTED_CALIBRATIONS

    def calibrate(self, key: int, image, face_coordonates):
        if self.SUPPORTED_CALIBRATIONS[key] in ['max_left_pupil', 'min_left_pupil']:
            self.__calibrate_eyes(self.SUPPORTED_CALIBRATIONS[key], image, face_coordonates)

    def __calibrate_eyes(self, which: str, image, face_coordonates):
        center, image_shape = self.__pupil_detector.find(image, face_coordonates)
        if center is False:
            return
        if which == 'max_left_pupil':
            self.calibrated_model.eye_max_left = center[0]
        elif which == 'min_left_pupil':
            self.calibrated_model.eye_max_right = center[0]