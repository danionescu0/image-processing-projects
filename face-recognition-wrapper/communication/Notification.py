from enum import Enum


class Notification(Enum):
    FACE_FOUND = 'face-found'
    FACE_ADDED = 'face-processed'
    FACE_DELETED = 'delete-face'