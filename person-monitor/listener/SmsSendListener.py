from pydispatch import dispatcher

from communication.SmsSender import SmsSender
from lock.ConfiguredTimedLock import ConfiguredTimedLock
from event.FacesFound import FacesFound
from listener.BaseListener import BaseListener
from service.MessageGenerator import MessageGenerator


class SmsSendListener(BaseListener):
    def __init__(self, sms_sender: SmsSender, timed_lock: ConfiguredTimedLock,
                 message_generator: MessageGenerator) -> None:
        self.__message_generator = message_generator
        self.__sms_sender = sms_sender
        self.__timed_lock = timed_lock

    def connect(self):
        dispatcher.connect(self.listen, signal="face_found", sender=dispatcher.Any)

    def listen(self, event: FacesFound):
        if self.__timed_lock.has_lock():
            return
        self.__sms_sender.send(self.get_text(event))
        self.__timed_lock.set_lock()

    # @todo refactore duplcate code
    def get_text(self, event: FacesFound):
        body = 'The following users have been found: '
        for user in event.users:
            if user.user_id is None:
                body += 'unknown, '
            else:
                body += user.user_name + ', '

        return body