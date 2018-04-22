from typing import List


class User:
    def __init__(self, id: str, name: str) -> None:
        self.id = id
        self.name = name
        self._image_ids = []

    @property
    def image_ids(self) -> List[str]:
        return self._image_ids

    @image_ids.setter
    def image_ids(self, value: List[str]):
        self._image_ids = value

    def __str__(self) -> str:
        return 'Id: {0}, Name: {1}, Images: {2}'.format(self.id, self.name, self._image_ids)