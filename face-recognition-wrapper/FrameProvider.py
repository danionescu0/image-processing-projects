import cv2
import imutils
import time


class FrameProvider:
    def __init__(self, camera: str, config: dict, resolution: tuple) -> None:
        self.__camera = camera
        self.__config = config
        self.__resolution = resolution
        self.__cap = None
        self.__ret = None
        self.__image = None

    def start(self):
        self.__cap = cv2.VideoCapture(0)
        time.sleep(2)
        self.__cap.set(3, self.__resolution[0])
        self.__cap.set(4, self.__resolution[1])

    def update_frame(self):
        ret, image = self.__cap.read()
        if ret:
            self.__image = image
        else:
            self.stop()
            self.start()

    def get_last_frame(self):
        if self.__config['use_percent_of_image'] != 100:
            self.__image = self.__get_cropped(self.__image)

        # rotate image as specified in config
        return imutils.rotate(self.__image, self.__config['rotate_camera_by'])

    #get image cropped from center
    def __get_cropped(self, image):
        height, width, channels = image.shape
        percent = 100 - self.__config['use_percent_of_image']
        start_x = int(width * percent / 100 / 2)
        end_x = width - start_x
        start_y = int(height * percent / 100 / 2)
        end_y = height - start_y

        return image[start_y:end_y, start_x:end_x]

    def stop(self):
        self.__cap.release()