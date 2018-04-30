from lock.TimedLock import TimedLock


class ConfiguredTimedLock:
    def __init__(self, key: str, seconds: int, timed_lock: TimedLock) -> None:
        self.__key = key
        self.__seconds = seconds
        self.__timed_lock = timed_lock

    def set_lock(self):
        self.__timed_lock.set_lock(self.__key, self.__seconds)

    def has_lock(self) -> bool:
        return self.__timed_lock.has_lock(self.__key)