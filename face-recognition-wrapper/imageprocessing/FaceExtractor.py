import ntpath
import os

import cv2
import face_recognition
import imutils


class FaceExtractor:
    def __init__(self, images_folder: str) -> None:
        self.__face_cache = {}
        self.__images_folder = images_folder

    def process(self, file_path: str, file_id: str):
        faces = self.__extract_faces(file_path)
        if len(faces) != 1:
            raise Exception("Nr of faces in imageprocessing is not 1")
        file = cv2.imread(file_path)
        print(file_path)
        file = imutils.resize(file, width=1024)
        face = faces[0]
        cropped = file[face[0]:face[2], face[3]:face[1]]
        file_extension = ntpath.basename(file_path).split('.')[1]
        new_file_path = os.path.join(self.__images_folder, file_id + '.' + file_extension)
        print(new_file_path)
        cv2.imwrite(new_file_path, cropped)

    def is_valid(self, file_path: str) -> dict:
        faces = self.__extract_faces(file_path)
        status = True
        error = ''
        if len(faces) == 0:
            status = False
            error = 'No faces found'
        elif len(faces) > 1:
            status = False
            error = 'Only one face per picture is admited'

        return {
            'status': status,
            'error': error
        }

    def __extract_faces(self, file_path):
        if file_path in self.__face_cache:
            return self.__face_cache[file_path]
        file = cv2.imread(file_path)
        file = imutils.resize(file, width=1024)
        rgb_file = file[:, :, ::-1]
        self.__face_cache[file_path] = face_recognition.face_locations(rgb_file)

        return self.__face_cache[file_path]