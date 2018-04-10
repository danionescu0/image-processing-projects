from enum import Enum


class Notification(Enum):
    FACE_FOUND = 'face-found'
    FACE_PROCESSED = 'face-processed'
    DELETE_FACE = 'delete-face'