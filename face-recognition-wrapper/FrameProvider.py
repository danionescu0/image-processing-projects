import cv2
import imutils


class FrameProvider:
    def __init__(self, camera: str, config: dict, resolution: tuple) -> None:
        # self.__video_stream = video_stream
        self.__camera = camera
        self.__config = config
        self.__resolution = resolution
        self.__cap = None

    def start(self):
        self.__cap = cv2.VideoCapture(0)
        self.__cap.set(3, self.__resolution[0])
        self.__cap.set(4, self.__resolution[1])
        # return self.__video_stream.start()

    def read(self):
        ret, image = self.__cap.read()
        if self.__config['use_percent_of_image'] != 100:
            image = self.__get_cropped(image)

        # rotate image as specified in config
        return imutils.rotate(image, self.__config['rotate_camera_by'])

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
        self.__video_stream.stop()