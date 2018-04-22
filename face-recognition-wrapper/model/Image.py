class Image:
    def __init__(self, id: str, file) -> None:
        self.id = id
        self.file = file

    def __str__(self) -> str:
        return 'Id: {0}, Name: {1}'.format(self.id)