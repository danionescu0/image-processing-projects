from pydispatch import dispatcher

from communication.EmailNotifier import EmailNotifier
from lock.ConfiguredTimedLock import ConfiguredTimedLock
from event.FacesFound import FacesFound
from listener.BaseListener import BaseListener


class EmailAlertListener(BaseListener):
    def __init__(self, email_notifier: EmailNotifier, timed_lock: ConfiguredTimedLock, address: str) -> None:
        self.__email_notifier = email_notifier
        self.__timed_lock = timed_lock
        self.__address = address

    def connect(self):
        dispatcher.connect(self.listen, signal="face_found", sender=dispatcher.Any)

    def listen(self, event: FacesFound):
        if self.__timed_lock.has_lock():
            return
        self.__email_notifier.send_alert(
            self.__address,
            "Persons found",
            self.__get_email_body(event),
            [('image.jpg', event.image)]
        )
        self.__timed_lock.set_lock()

    def __get_email_body(self, event: FacesFound):
        body = 'The following users have been found: '
        for user in event.users:
            if user.user_id is None:
                body += 'unknown, '
            else:
                body += user.user_name + ', '

        return body