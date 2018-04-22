import json
import base64

from pydispatch import dispatcher

from communication.MqttConnection import MqttConnection
from event.FaceFound import FaceFound


class FaceFoundListener:
    TYPE = 'face-found'

    def __init__(self, connection: MqttConnection) -> None:
        self.__connection = connection

    def listen(self):
        self.__connection.listen(self.__do_listen)

    def __do_listen(self, message):
        data = json.loads(message.decode())
        callback_type = data['type']
        decoded_data = data['data']
        if callback_type != self.TYPE:
            return
        decoded_file = base64.b64decode(decoded_data['image'].encode('utf-8'))
        face_found = FaceFound(
            decoded_file, decoded_data['user_name'], decoded_data['user_id'],
            (decoded_data['right_px'], decoded_data['top_px']),
            (decoded_data['left_px'], decoded_data['bottom_px'],)
        )
        dispatcher.send(FaceFound.NAME, event=face_found)