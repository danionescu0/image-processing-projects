class CalibratedModel:
    def __init__(self, eye_max_left: int = None, eye_max_right: int = None,
                 mouth_closed_height: int = None, mouth_opened_height: int = None) -> None:
        self.eye_max_left = eye_max_left
        self.eye_max_right = eye_max_right
        self.mouth_closed_height = mouth_closed_height
        self.mouth_opened_height = mouth_opened_height

    def __repr__(self) -> str:
        return 'Eye left: {0}, Eye right: {1}, Mouth closed: {2}, Mouth opened: {3}'\
            .format(self.eye_max_left, self.eye_max_right, self.mouth_closed_height, self.mouth_opened_height)