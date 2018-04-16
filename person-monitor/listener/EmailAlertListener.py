from pydispatch import dispatcher

from communication.EmailNotifier import EmailNotifier
from event.FaceFound import FaceFound
from listener.BaseListener import BaseListener


class EmailAlertListener(BaseListener):
    def __init__(self, email_notifier: EmailNotifier) -> None:
        self.__email_notifier = email_notifier

    def connect(self):
        dispatcher.connect(self.listen, signal="face_found", sender=dispatcher.Any)

    def listen(self, event: FaceFound):
        print(event)