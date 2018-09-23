import base64

import cv2


class ImageEncoder:
    def encode_numpy_image(self, numpy_image) -> str:
        return self.__get_encoded(cv2.imencode('.jpg', numpy_image)[1])

    def encode_image_file(self, file_path: str) -> str:
        with open(file_path, 'rb') as open_file:
            return self.__get_encoded(open_file.read())

    def __get_encoded(self, binary_file):
        return base64.b64encode(binary_file).decode('utf-8')