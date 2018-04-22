import abc
from typing import List
from model.DetectedFace import DetectedFace


class FaceDetector(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def find(self, image) -> List[DetectedFace]:
        pass

    @abc.abstractmethod
    def load_face(self, filepath: str):
        pass

    @abc.abstractmethod
    def load_faces(self, filepaths: List[str]):
        pass

    @abc.abstractmethod
    def delete_face(self, filepath: str):
        pass