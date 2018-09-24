# email credentials, will be used to send an email
email = {
    'sender_addr': 'ionescu.dan84@gmail.com',
    'sender_password': 'octombrie8',
    'notified_address': 'dan.ionescu@machteamsoft.ro',
    'min_time_between_emails': 50,
    'enabled': True
}

# devicehub api_key, project etc, for logging the data as a devicehub sensor
devicehub = {
    'api_key': 'ed16df23-36e4-4507-94d0-654af8172e58',
    'device_uuid': 'e62fbb50-9fca-4188-8a3a-92d8452c7e66',
    'project_id': '4',
    'user_id_to_sensor_mapping': {
        '23': 'Dan'
    },
    'enabled': True
}

text_to_speech = {
    'host': 'http://192.168.0.107:80',
    'user': 'test_user',
    'password' : 'test_pass',
    'enabled': True
}

mqtt = {
    'host': '192.168.0.100',
    'port': 1884, # mosquitto default port
    'user': 'username',
    'password': 'password'
}