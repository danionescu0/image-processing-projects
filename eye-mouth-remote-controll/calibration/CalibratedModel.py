class CalibratedModel:
    def __init__(self, eye_max_left: int = None, eye_max_right: int = None,
                 mouth_closed_height: int = None, mouth_opened_height: int = None) -> None:
        self.eye_max_left = eye_max_left
        self.eye_max_right = eye_max_right
        self.mouth_closed_height = mouth_closed_height
        self.mouth_opened_height = mouth_opened_height

    def is_calibrated(self) -> bool:
        return self.eye_max_right is not None and self.eye_max_left is not None \
               and self.mouth_opened_height is not None and self.mouth_closed_height is not None

    def __repr__(self) -> str:
        return 'Calibrated Model: Eye left: {0}, Eye right: {1}, Mouth closed: {2}, Mouth opened: {3}'\
            .format(self.eye_max_left, self.eye_max_right, self.mouth_closed_height, self.mouth_opened_height)