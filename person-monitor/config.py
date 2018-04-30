email = {
    'sender_addr': '',
    'sender_password': '',
    'notified_address': '',
    'min_time_between_emails': 50,
    'enabled': True
}

devicehub = {
    'api_key': '',
    'device_uuid': '',
    'project_id': '',
    'user_id_to_sensor_mapping': {
        '23': 'Dan'
    },
    'enabled': True
}

mqtt = {
    'host': '192.168.0.105',
    'port': 1883, # mosquitto default port
    'user': 'user',
    'password': 'your_password'
}

mongodb_uri = 'mongodb://localhost:27017/'