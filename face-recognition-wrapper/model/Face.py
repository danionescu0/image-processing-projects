class Face:
    def __init__(self, id: str, top: int, right: int, bottom: int, left:int) -> None:
        self.id = id
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left

    def __str__(self) -> str:
        return 'Id: {0}, Top: {1}, Right: {2}, Bottom: {3}, Left: {4}'\
            .format(self.id, self.top, self.right, self.bottom, self.left)