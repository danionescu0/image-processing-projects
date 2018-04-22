import time


# def save_image(message):
#     data = json.loads(message.decode())
#
#     encoded_bytes = data['data']['image'].encode('utf-8')
#     del data['data']['image']
#     print(data)
#     with open('test.jpg', 'wb') as thefile:
#         thefile.write(base64.b64decode(encoded_bytes))
#
#
# mqtt_connection = MqttConnection(config.mqtt['host'], config.mqtt['port'], config.mqtt['user'], config.mqtt['password'])
# mqtt_connection.listen(save_image)
# mqtt_connection.connect()
# while True:
#     pass
#


