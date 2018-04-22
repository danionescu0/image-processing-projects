from lock.TimedLock import TimedLock


class EmailTimedLock:
    __KEY = 'email'

    def __init__(self, timed_lock: TimedLock, min_time_between_emails: int) -> None:
        self.__timed_lock = timed_lock
        self.__min_time_between_emails = min_time_between_emails

    def set_lock(self):
        self.__timed_lock.set_lock(self.__KEY, self.__min_time_between_emails)

    def has_lock(self) -> bool:
        return self.__timed_lock.has_lock(self.__KEY)