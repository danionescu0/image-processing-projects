import os
import base64
import random

import cv2


class ImageEncoder:
    def __init__(self, temporary_path) -> None:
        self.__temporary_path = temporary_path

    # @Todo find a more elegant implementation for this
    def encode_numpy_image(self, numpy_image) -> str:
        name = str(random.randint(10000, 9000000)) + '.jpg'
        new_file_path = os.path.join(self.__temporary_path, name)
        cv2.imwrite(new_file_path, numpy_image)
        encoded_file = self.encode_image_file(new_file_path)
        os.remove(new_file_path)

        return encoded_file

    def encode_image_file(self, file_path: str) -> str:
        with open(file_path, 'rb') as open_file:
            encoded = base64.b64encode(open_file.read()).decode('utf-8')
            return encoded