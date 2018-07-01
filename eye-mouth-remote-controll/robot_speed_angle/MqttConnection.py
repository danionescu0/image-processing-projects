import paho.mqtt.client as mqtt


class MqttConnection():
    __MOVEMENT_CHANNEL = 'robot/movement'

    def __init__(self, host : str, port : str, user : str, password : str):
        self.__host = host
        self.__port = port
        self.__user = user
        self.__password = password
        self.__client = None

    def connect(self):
        self.__client = mqtt.Client()

        def on_connect(client, userdata, flags, rc):
            self.__client.subscribe(self.__MOVEMENT_CHANNEL)

        self.__client.on_connect = on_connect
        self.__client.username_pw_set(self.__user, self.__password)
        self.__client.connect_async(self.__host, self.__port, 60)
        self.__client.loop_start()

    def send_movement_command(self, message : str):
        self.__client.publish(self.__MOVEMENT_CHANNEL, message, 2)