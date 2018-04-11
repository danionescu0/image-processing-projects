import cv2
import json
import base64

import imutils

import config
from communication.MqttConnection import MqttConnection

def save_image(message):
    data = json.loads(message.decode())

    encoded_bytes = data['data']['image'].encode('utf-8')
    print (encoded_bytes)
    with open('test.jpg', 'wb') as thefile:
        thefile.write(base64.b64decode(encoded_bytes))


mqtt_connection = MqttConnection(config.mqtt['host'], config.mqtt['port'], config.mqtt['user'], config.mqtt['password'])
mqtt_connection.listen(save_image)
mqtt_connection.connect()
while True:
    pass

source_file = './temp/4343.jpg'
dest_file = './temp/hihihi.jpg'
# with open(source_file, 'rb') as open_file:
#     image_disc = open_file.read()
#     print(image_disc)
#     image_bytes = base64.b64encode(image_disc)
#     print(image_bytes)
#     image_str = image_bytes.decode('utf-8')
#
#     print(image_str)
#     print ('reversing')
#
#     encoded_bytes = image_str.encode('utf-8')
#     print(encoded_bytes)
#     decoded_from_base_64 = base64.b64decode(encoded_bytes)
#
#     print(decoded_from_base_64)
#     with open(dest_file, "wb") as myfile:
#         myfile.write(decoded_from_base_64)


