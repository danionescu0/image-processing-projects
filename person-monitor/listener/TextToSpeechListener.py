from pydispatch import dispatcher

from communication.TextToSpeech import TextToSpeech
from lock.ConfiguredTimedLock import ConfiguredTimedLock
from event.FacesFound import FacesFound
from listener.BaseListener import BaseListener
from service.MessageGenerator import MessageGenerator


class TextToSpeechListener(BaseListener):
    def __init__(self, text_to_speech: TextToSpeech, timed_lock: ConfiguredTimedLock,
                 message_generator: MessageGenerator) -> None:
        self.__message_generator = message_generator
        self.__text_to_speech = text_to_speech
        self.__timed_lock = timed_lock

    def connect(self):
        dispatcher.connect(self.listen, signal="face_found", sender=dispatcher.Any)

    def listen(self, event: FacesFound):
        if self.__timed_lock.has_lock():
            return
        self.__text_to_speech.say(self.__message_generator.get_text(event))
        self.__timed_lock.set_lock()