# Person monitor


In this project we're going to implement a real time person monitor with email notification,
text to speech and DeviceHub integrations.

We're going to receive face notification from "Face recognition wrapper" over MQTT and react
to them by:

- sending email with known/unknown person along with a picture

- use a text to speech API to communicate by voice 



### Installing dependencies & configure

*Alternatively you can use docker*

* Edit config.py and configure MQTT, and other settings if needed

* Details about sending email with gmail: http://stackabuse.com/how-to-send-emails-with-gmail-using-python/

* Install python requirements (use a virtualenv)
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

* Configure text to speech

````
text_to_speech = {
    'host': 'http://ip_address',
    'user': 'user',
    'password' : 'pass',
    'enabled': True
}
````

As a remote speaker we'll be using the following project: https://www.instructables.com/id/How-to-Build-a-Text-to-Speech-IOT-Speaker/

After setting up the project configure, host, user and password

* Run the project:

````
python background.py
````