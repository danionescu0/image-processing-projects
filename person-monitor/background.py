import config
from communication.MqttConnection import MqttConnection
from communication.EmailNotifier import EmailNotifier
from communication.FaceFoundListener import FaceFoundListener
from communication.TextToSpeech import TextToSpeech
from communication.SmsSender import SmsSender
from listener.ListenerContainer import ListenerContainer
from listener.EmailAlertListener import EmailAlertListener
from listener.TextToSpeechListener import TextToSpeechListener
from listener.SmsSendListener import SmsSendListener
from lock.TimedLock import TimedLock
from lock.ConfiguredTimedLock import ConfiguredTimedLock
from service.MessageGenerator import MessageGenerator


listener_container = ListenerContainer()
message_generator = MessageGenerator()


#configure email notifier
if config.email['enabled']:
    email_timed_lock = ConfiguredTimedLock('email', config.email['min_time_between_emails'], TimedLock())
    email_notifier = EmailNotifier(config.email['sender_addr'], config.email['sender_password'])

    email_alert_listener = EmailAlertListener(email_notifier, email_timed_lock,
                                              config.email['notified_address'], message_generator)
    listener_container.register_listener(email_alert_listener)

#configure local text to speech notifier
if config.text_to_speech['enabled']:
    text_to_speech = TextToSpeech(config.text_to_speech['host'], config.text_to_speech['user'],
                                  config.text_to_speech['password'])
    tts_timed_lock = ConfiguredTimedLock('tts', 50, TimedLock())
    listener_container.register_listener(TextToSpeechListener(text_to_speech, tts_timed_lock, message_generator))

#configure sms sender
if config.sms['enabled']:
    sms_sender = SmsSender(config.sms['url'])
    sms_timed_lock = ConfiguredTimedLock('tts', 50, TimedLock())
    listener_container.register_listener(SmsSendListener(sms_sender, sms_timed_lock, message_generator))

listener_container.initialise()



mqtt_connection = MqttConnection(config.mqtt['host'], config.mqtt['port'], config.mqtt['user'], config.mqtt['password'])
face_found_listener = FaceFoundListener(mqtt_connection)
face_found_listener.listen()
mqtt_connection.connect()