import config
from communication.MqttConnection import MqttConnection
from communication.EmailNotifier import EmailNotifier
from communication.FaceFoundListener import FaceFoundListener
from listener.ListenerContainer import ListenerContainer
from listener.EmailAlertListener import EmailAlertListener
from lock.TimedLock import TimedLock
from lock.EmailTimedLock import EmailTimedLock

email_timed_lock = EmailTimedLock(TimedLock(), config.email['min_time_between_emails'])

email_notifier = EmailNotifier(config.email['sender_addr'], config.email['sender_password'])
email_alert_listener = EmailAlertListener(email_notifier, email_timed_lock, config.email['notified_address'])
listener = ListenerContainer()
listener.register_listener(email_alert_listener)
listener.initialise()


mqtt_connection = MqttConnection(config.mqtt['host'], config.mqtt['port'], config.mqtt['user'], config.mqtt['password'])
face_found_listener = FaceFoundListener(mqtt_connection)
face_found_listener.listen()
mqtt_connection.connect()