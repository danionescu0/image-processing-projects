import json
import base64

from pydispatch import dispatcher

from communication.MqttConnection import MqttConnection
from event.FacesFound import FacesFound
from model.User import User


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
        users = [
                    User(face_data['user_name'], face_data['user_id'],
                       (face_data['right_px'], face_data['top_px']),
                       (face_data['left_px'], face_data['bottom_px']))
                      for face_data in decoded_data['faces']
            ]
        dispatcher.send(FacesFound.NAME, event=FacesFound(decoded_file, users))