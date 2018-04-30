from pydispatch import dispatcher

from communication.EmailNotifier import EmailNotifier
from lock.ConfiguredTimedLock import ConfiguredTimedLock
from event.FaceFound import FaceFound
from listener.BaseListener import BaseListener


class EmailAlertListener(BaseListener):
    def __init__(self, email_notifier: EmailNotifier, timed_lock: ConfiguredTimedLock, address: str) -> None:
        self.__email_notifier = email_notifier
        self.__timed_lock = timed_lock
        self.__address = address

    def connect(self):
        dispatcher.connect(self.listen, signal="face_found", sender=dispatcher.Any)

    def listen(self, event: FaceFound):
        if self.__timed_lock.has_lock():
            return
        self.__email_notifier.send_alert(
            self.__address,
            "Face found",
            self.__get_email_body(event),
            [('first_person.jpg', event.image)]
        )
        self.__timed_lock.set_lock()

    def __get_email_body(self, event: FaceFound):
        body = ''
        if event.user_id is None:
            body += 'An unknown face has been found'
        else:
            body += 'User with user_name: {0} has been found'.format(event.user_name)

        return body