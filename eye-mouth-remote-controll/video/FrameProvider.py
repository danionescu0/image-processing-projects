import queue
import time
from multiprocessing import Process

import cv2


class FrameProvider(Process):
    def __init__(self, camera_device: str, frame) -> None:
        Process.__init__(self)
        self.__camera_device = camera_device
        self.__video_capture = None
        self.__frame = frame

    def run(self):
        self.__video_capture = cv2.VideoCapture(self.__camera_device)
        while True:
            ret, frame = self.__video_capture.read()
            try:
                self.__frame.get(False)
            except queue.Empty:
                  pass
            try:
                self.__frame.put(frame, False)
            except queue.Full:
                pass
            time.sleep(0.05)
            if ret is not True:
                raise Exception("Video frame not available from opencv")

    def stop(self):
        self.__video_capture.release()