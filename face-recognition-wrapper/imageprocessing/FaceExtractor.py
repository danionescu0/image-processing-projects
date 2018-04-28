import ntpath

import cv2
import face_recognition
import imutils

from imageprocessing.FacePaths import FacePaths


class FaceExtractor:
    def __init__(self, face_paths: FacePaths) -> None:
        self.__face_cache = {}
        self.__face_paths = face_paths

    def process(self, file_path: str, face_id: str) -> str:
        faces = self.__extract_faces(file_path)
        if len(faces) != 1:
            raise Exception("Nr of faces in imageprocessing is not 1")
        high_res_img = cv2.imread(file_path)
        high_res_img = imutils.resize(high_res_img, width=FacePaths.RESOLUTION_HIGH)
        face = faces[0]
        cropped = high_res_img[face[0]:face[2], face[3]:face[1]]
        file_extension = ntpath.basename(file_path).split('.')[1]
        high_resolution_path = self.__face_paths.get_high_resolution(face_id, file_extension)
        cv2.imwrite(high_resolution_path, cropped)
        low_res_img = imutils.resize(cropped, width=FacePaths.RESOLUTION_LOW)
        cv2.imwrite(self.__face_paths.get_low_resolution(face_id, file_extension), low_res_img)

        return high_resolution_path

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
        file = imutils.resize(file, width=FacePaths.RESOLUTION_HIGH)
        rgb_file = file[:, :, ::-1]
        self.__face_cache[file_path] = face_recognition.face_locations(rgb_file)

        return self.__face_cache[file_path]