from typing import List

import face_recognition

from FaceDetector import FaceDetector


class FaceRecognition(FaceDetector):
    def __init__(self):
        self.__known_face_encodings = []
        self.__known_face_filenames = []

    def find(self, image) -> List:
        rgb_frame = image[:, :, ::-1]
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        faces = []
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.__known_face_encodings, face_encoding)
            # If a match was found in known_face_encodings, just use the first one
            name = None
            if True in matches:
                first_match_index = matches.index(True)
                print(face_locations, first_match_index, matches)
                name = self.__known_face_filenames[first_match_index]
            faces.append((name, top, right, bottom, left))

        return faces

    def load_face(self, file: str):
        image = face_recognition.load_image_file(file)
        self.__known_face_encodings.append(face_recognition.face_encodings(image)[0])
        self.__known_face_filenames.append(file)

    def load_faces(self, files: List[str]):
        [self.load_face(file) for file in files]

    def delete_face(self, file: str):
        pass