from face_detection.FaceModel import FaceModel


class MouthAnalizer:
    def __init__(self) -> None:
        super().__init__()

    def get_height(self, face_model: FaceModel) -> int:
        mouth = face_model.get_mouth()
        min_height = min(mouth, key=lambda coordonates: coordonates[1])[1]
        max_height = max(mouth, key=lambda coordonates: coordonates[1])[1]

        return max_height - min_height