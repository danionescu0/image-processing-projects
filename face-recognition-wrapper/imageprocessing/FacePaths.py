import os


class FacePaths:
    RESOLUTION_HIGH = 1024
    RESOLUTION_LOW = 300

    def __init__(self, images_folder: str) -> None:
        self.__images_folder = images_folder

    def get_high_resolution(self, face_id: str, file_extension: str) -> str:
        return os.path.join(self.__images_folder, face_id + '.' + file_extension)

    def get_low_resolution(self, face_id: str, file_extension: str) -> str:
        return os.path.join(self.__images_folder, face_id + '_thumb.' + file_extension)