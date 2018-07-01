class Coordonates:
    def __init__(self, eyes_horizontal_angle: int = None, mouth_vertical_percent: int = None) -> None:
        self.eyes_horizontal_angle = eyes_horizontal_angle
        self.mouth_vertical_percent = mouth_vertical_percent

    def has_detection(self) -> bool:
        return self.eyes_horizontal_angle is not None

    def __repr__(self) -> str:
        return 'Eyes horizontal angle: {0}, Mouth vertical percent: {1}'\
            .format(self.eyes_horizontal_angle, self.mouth_vertical_percent)