import abc
from typing import List
from model.Face import Face


class FaceDetector(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def find(self, image) -> List[Face]:
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