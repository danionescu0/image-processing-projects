import config
from communication.MqttConnection import MqttConnection
from communication.EmailNotifier import EmailNotifier
from communication.FaceFoundListener import FaceFoundListener
from communication.DevicehubSensorNotifier import DevicehubSensorNotifier
from listener.ListenerContainer import ListenerContainer
from listener.EmailAlertListener import EmailAlertListener
from listener.DevicehubListener import DevicehubListener
from lock.TimedLock import TimedLock
from lock.EmailTimedLock import EmailTimedLock
from lock.ConfiguredTimedLock import ConfiguredTimedLock

listener = ListenerContainer()
email_timed_lock = EmailTimedLock(TimedLock(), config.email['min_time_between_emails'])
email_notifier = EmailNotifier(config.email['sender_addr'], config.email['sender_password'])

if config.email['enabled']:
    email_alert_listener = EmailAlertListener(email_notifier, email_timed_lock, config.email['notified_address'])
    listener.register_listener(email_alert_listener)

if config.devicehub['enabled']:
    devicehub_sensor_notifier = DevicehubSensorNotifier(config.devicehub['api_key'], config.devicehub['project_id'])
    devicehub_timed_lock = ConfiguredTimedLock('devicehub', 60, TimedLock())
    devicehub_alert_listener = DevicehubListener(devicehub_timed_lock, devicehub_sensor_notifier,
                                                 config.devicehub['device_uuid'],
                                                 config.devicehub['user_id_to_sensor_mapping'])
    listener.register_listener(devicehub_alert_listener)

listener.initialise()


mqtt_connection = MqttConnection(config.mqtt['host'], config.mqtt['port'], config.mqtt['user'], config.mqtt['password'])
face_found_listener = FaceFoundListener(mqtt_connection)
face_found_listener.listen()
mqtt_connection.connect()