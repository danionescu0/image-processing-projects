class User:
    def __init__(self, id: str, name: str) -> None:
        self.id = id
        self.name = name

    def __str__(self) -> str:
        return 'Id: {0}, Name: {1}'.format(self.id, self.name)