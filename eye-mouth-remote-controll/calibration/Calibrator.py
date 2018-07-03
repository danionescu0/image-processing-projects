from calibration.CalibratedModel import CalibratedModel
from PupilDetector import PupilDetector


class Calibrator:
    SUPPORTED_CALIBRATIONS = {
        82: 'max_left_pupil',
        83: 'min_left_pupil',
        84: 'mounth_closed',
        85: 'mouth_opened',
    }

    def __init__(self, pupil_detector: PupilDetector) -> None:
        self.pupil_detector = pupil_detector
        self.calibratedModel = CalibratedModel()

    def supports_calibration(self, key: int) -> bool:
        return key in self.SUPPORTED_CALIBRATIONS

    def set_calibration(self, key: int, image, face_coordonates):
        self.calibratedModel.eye_max_right = 50