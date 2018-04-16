import config
from communication.MqttConnection import MqttConnection

mqtt_connection = MqttConnection(config.mqtt['host'], config.mqtt['port'], config.mqtt['user'], config.mqtt['password'])
mqtt_connection.connect()