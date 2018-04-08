import abc
from typing import Tuple
from typing import List


class FaceDetector(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def find(self, image) -> List:
        pass

    @abc.abstractmethod
    def load_face(self, file: str):
        pass

    @abc.abstractmethod
    def load_faces(self, file: List[str]):
        pass

    @abc.abstractmethod
    def delete_face(self, file: str):
        pass