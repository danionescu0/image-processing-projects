# email credentials, will be used to send an email
email = {
    'sender_addr': 'replace_with_own',
    'sender_password': 'replace_with_own',
    'notified_address': 'replace_with_own',
    'min_time_between_emails': 50,
    'enabled': True
}

# devicehub api_key, project etc, for logging the data as a devicehub sensor
devicehub = {
    'api_key': 'replace_with_own',
    'device_uuid': 'replace_with_own',
    'project_id': 'replace_with_own',
    'user_id_to_sensor_mapping': {
        'replace_with_own': 'replace_with_own'
    },
    'enabled': True
}

mqtt = {
    'host': '192.168.0.100',
    'port': 1883, # mosquitto default port
    'user': 'username',
    'password': 'password'
}

mongodb_uri = 'mongodb://localhost:27017/'