from typing import Tuple


class User:
    def __init__(self, user_name: str, user_id: str, top_right_coordonates: Tuple[int, int],
                 bottom_left_coordonates: Tuple[int, int]) -> None:
        self.user_name = user_name
        self.user_id = user_id
        self.top_right_coordonates = top_right_coordonates
        self.bottom_left_coordonates = bottom_left_coordonates

    def __str__(self) -> str:
        return 'Username: {0}, Userid: {1}, Top_right: {2}, Bottom_left: {3}'\
            .format(self.user_name, self.user_id, self.top_right_coordonates, self.bottom_left_coordonates)