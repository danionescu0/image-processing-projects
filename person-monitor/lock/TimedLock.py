import time


class TimedLock:
    def __init__(self) -> None:
        self.__locks = {}

    def set_lock(self, key: str, seconds: int):
        self.__locks[key] = (time.time(), seconds)

    def has_lock(self, key: str) -> bool:
        if key not in self.__locks:
            return False

        record = self.__locks[key]
        timediff = time.time() - record[0]
        if timediff > record[1]:
            self.__locks.pop(key)
            return False

        return True

