from pydispatch import dispatcher


import config
from communication.MqttConnection import MqttConnection
from communication.EmailNotifier import EmailNotifier
from event.FaceFound import FaceFound
from listener.ListenerContainer import ListenerContainer
from listener.EmailAlertListener import EmailAlertListener


email_notifier = EmailNotifier(config.email['notified_address'], config.email['sender_password'])
email_alert_listener = EmailAlertListener(email_notifier)
listener = ListenerContainer()
listener.register_listener(email_alert_listener)
listener.initialise()


mqtt_connection = MqttConnection(config.mqtt['host'], config.mqtt['port'], config.mqtt['user'], config.mqtt['password'])
mqtt_connection.connect()

print('sending')
dispatcher.send(FaceFound.NAME, event=FaceFound("xx", "test_name", "test_id", (1, 2), (3, 4)))