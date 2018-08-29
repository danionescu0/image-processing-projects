from pydispatch import dispatcher

from communication.TextToSpeech import TextToSpeech
from lock.ConfiguredTimedLock import ConfiguredTimedLock
from event.FacesFound import FacesFound
from listener.BaseListener import BaseListener


class TextToSpeechListener(BaseListener):
    def __init__(self, text_to_speech: TextToSpeech, timed_lock: ConfiguredTimedLock) -> None:
        self.__text_to_speech = text_to_speech
        self.__timed_lock = timed_lock

    def connect(self):
        dispatcher.connect(self.listen, signal="face_found", sender=dispatcher.Any)

    def listen(self, event: FacesFound):
        if self.__timed_lock.has_lock():
            return
        self.__text_to_speech.say(self.get_text(event))
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