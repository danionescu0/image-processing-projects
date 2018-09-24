import imutils
from imutils.video import VideoStream


class FrameProvider:
    def __init__(self, video_stream: VideoStream, config: dict) -> None:
        self.__video_stream = video_stream
        self.__config = config

    def start(self):
        return self.__video_stream.start()

    def update(self):
        self.__video_stream.update()

    def read(self):
        image = self.__video_stream.read()
        if self.__config['use_percent_of_image'] != 100:
            image = self.__get_cropped(image)

        # resize image as specified in config
        frame = imutils.resize(image, width=self.__config['resize_image_by_width'])

        # rotate image as specified in config
        return imutils.rotate(frame, self.__config['rotate_camera_by'])

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