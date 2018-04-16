from typing import Tuple


class FaceFound:
    NAME = 'face_found'

    def __init__(self, image, user_name: str, user_id: str, top_right: Tuple[int, int], bottom_left: Tuple[int, int]) -> None:
        self.image = image
        self.user_name = user_name
        self.user_id = user_id
        self.top_right = top_right
        self.bottom_left = bottom_left

    def __str__(self) -> str:
        return 'Username: {0}, Userid: {1}, Top_right: {2}, Bottom_left: {3}'\
            .format(self.user_name, self.user_id, self.top_right, self.bottom_left)

