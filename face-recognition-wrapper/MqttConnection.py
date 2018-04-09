import paho.mqtt.client as mqtt


class MqttConnection():
    FACES_CHANNEL = 'faces/found'
    NOTIFICATIONS_CHANNEL = 'notifications'

    def __init__(self, host : str, port : str, user : str, password : str):
        self.__host = host
        self.__port = port
        self.__user = user
        self.__password = password

    def connect(self):
        self.client = mqtt.Client()

        def on_connect(client, userdata, flags, rc):
            self.client.subscribe(self.NOTIFICATIONS_CHANNEL)

        self.client.on_connect = on_connect
        # self.client.username_pw_set(self.__user, self.__password)
        self.client.connect_async(self.__host, self.__port, 60)
        self.client.loop_start()

    def send(self, channel : str, message : str):
        self.client.publish(channel, message, 2)