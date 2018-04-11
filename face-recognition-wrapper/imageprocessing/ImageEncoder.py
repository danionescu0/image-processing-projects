import os
import base64
import random

import cv2


class ImageEncoder:
    def __init__(self, temporary_path) -> None:
        self.__temporary_path = temporary_path

    # @Todo find a more elegant implementation for this
    def encode(self, numpy_image) -> str:
        name = str(random.randint(10000, 9000000)) + '.jpg'
        new_file_path = os.path.join(self.__temporary_path, name)
        cv2.imwrite(new_file_path, numpy_image)

        with open(new_file_path, 'rb') as open_file:
            encoded = base64.b64encode(open_file.read()).decode('utf-8')
            os.remove(new_file_path)
            return encoded