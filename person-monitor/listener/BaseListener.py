import abc

from event.FaceFound import FaceFound


class BaseListener(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def connect(self):
        pass

    @abc.abstractmethod
    def listen(self, event: FaceFound):
        pass
