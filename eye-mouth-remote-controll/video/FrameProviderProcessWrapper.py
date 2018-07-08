from multiprocessing import Queue
import queue

from video.FrameProvider import FrameProvider


class FrameProviderProcessWrapper:
    def __init__(self, camera_device: str, rotation_angle: int) -> None:
        self.__camera_device = camera_device
        self.__rotation_angle = rotation_angle
        self.__frame = None
        self.__process = None

    def start(self):
        self.__frame = Queue(1)
        self.__process = FrameProvider(self.__camera_device, self.__rotation_angle, self.__frame)
        self.__process.daemon = True
        self.__process.start()

    def get_last_frame(self):
        if self.__frame.qsize() > 0:
            try:
                return self.__frame.get(True)
            except queue.Empty:
                return None

        return None

    def stop(self):
        self.__process.stop()