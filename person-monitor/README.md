# Person monitor


In this project we're going to implement a real time person monitor with email notification,
text to speech etc.

We're going to receive face notification from "Face recognition wrapper" over MQTT and react
to them by:

- sending email with known/unknown person along with a picture

- use a text to speech API to communicate by voice 

- track known persons on a graph using free IOT platforms like devicehub

- configure known persons, email notification etc etc in a graphical UI


### Installing dependencies & configure

* Edit config.py and configure mqtt, and other settings if needed

* Details about sending email with gmail: http://stackabuse.com/how-to-send-emails-with-gmail-using-python/

* Install python requirements:
````
pip install -r requirements.txt
````

* Mosquitto mqtt broker: https://mosquitto.org/download/

````
sudo apt-get install mosquitto
````

* Configure mqtt: host, port user and password in config.py

````
mqtt = {
    'host': 'ip',
    'port': 1883, # mosquitto default port
    'user': 'your_mqtt_user',
    'password': 'your_mqtt_password'
}
````

* Configure devicehub integration if desired

If you want to monitor the person in a nice GUI you can use the https://www.devicehub.net/ IOT platform.

Create an account there, obtain the API key then create a project, on that project create a device (obtain the device uuid), 
and for each person you want to monitor create an digital sensor.

Make sure enabled is set to True, then copy the api_key, the device_uuid and project id in the config.py

Then for each person you want to monitor and is registered in the face-recognition-wrapper, create a sensor and 
check it in under the dictionary key: 'user_id_to_sensor_mapping' like below:

````
devicehub = {
    'api_key': 'your_api_key',
    'device_uuid': 'your_device_uuid',
    'project_id': 'the_numeric_project_id',
    'user_id_to_sensor_mapping': {
        'some_user_id': 'some_sensor_from_devicehub',
        'some_other_user_id': 'some_other_sensor_from_devicehub',
        ...
    },
    'enabled': True
}
````

* Configure email alerts. These alerts will contain the captured frame containing a face, along with a user name if the 
face is found on the internal database;

You will need to configure the sender_addr, sender_password and notified_address

The key 'min_time_between_emails' means how often an email with an alert will be send

First make sure the enabled key is True

````
email = {
    'sender_addr': 'sender_gmail_address',
    'sender_password': 'sender_password',
    'notified_address': 'receiver_email_address',
    'min_time_between_emails': interval_in_seconds,
    'enabled': True
}
````