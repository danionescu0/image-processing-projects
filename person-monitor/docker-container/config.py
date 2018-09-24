# email credentials, will be used to send an email
email = {
    'sender_addr': '',
    'sender_password': '',
    'notified_address': '',
    'min_time_between_emails': 50,
    'enabled': True
}

# devicehub api_key, project etc, for logging the data as a devicehub sensor
devicehub = {
    'api_key': '',
    'device_uuid': '',
    'project_id': '',
    'user_id_to_sensor_mapping': {
        '23': 'Dan'
    },
    'enabled': True
}

text_to_speech = {
    'host': 'http://ip:80',
    'user': 'test_user',
    'password' : 'test_pass',
    'enabled': True
}

mqtt = {
    'host': 'mosquitto',
    'port': 1884, # mosquitto default port
    'user': 'username',
    'password': 'password'
}

mongodb_uri = 'mongodb://mongodb:27017/'