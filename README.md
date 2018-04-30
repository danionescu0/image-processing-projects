Projects:

1. [Face recognition wrapper](#Face recognition wrapper)

2. [Person monitor](#Person monitor)


#Face recognition wrapper

This library  uses a video stream (from a webcam or raspbery pi camera) to identify faces and match then against 
known persons and notify what has found using MQTT.

*Features:*

- face identification in video stream

- face matching against known persons faces

- it uses a configurable number of processing making use of all the cores in the system 

- HTTP API to creata, add delete user and faces

- MQTT notifications with face coordonates, person id (if found), and encoded image


The library is well suited for a development board like Raspberry pi and for a face tracking and face recognition.

#### Libraries used (special thanks) for image processing

[Opencv](https://github.com/opencv)

[Face recognition](https://github.com/ageitgey/face_recognition)

[Imutils](https://github.com/jrosebr1/imutils)


### Installing dependencies & configure

* Edit config.py and configure mqtt, and other settings if needed

* Install python requirements:
````
pip install -r requirements.txt
````

* Install mongodb and ensure and start it
````
sudo apt-get install mongodb
````

* Mosquitto mqtt broker: https://mosquitto.org/download/

````
sudo apt-get install mosquitto
````

* Configure mosquitto user and password and edit config.py and set the mosquitto user and password

### Running the project
activate virual environment if needed

* Start the web server
````
python webserver.py 
````
* Start the background process
````
python background.py 
````

### Creating users, deleting users, adding faces to users, deleting faces

HTTP API:

- create a person profile

- uploade a photo for the person

- delete a person photo

- delete a person


**Create new user**

POST request to: your_ip:8080/user/userid

GET parameters:

userid

POST parameters

"name" containing the user name

**Add new face to user**

POST request to: your_ip:8080/face/face_id

GET parameters:

"face_id": id of the face that will be stored in the db

POST parameters:

"user_id": to what user id does the face belongs

"photo": the file to be upladed (containing one face)

**Delete face for user**

DELETE request to: your_ip:8080/face/face_id

GET parameters:

"face_id": id of the face that will be stored in the db

**Get users with photos**

Get request to: your_ip:8080/users?page=1

GET parameters:

"page" the page number to be returned

### Listen to mqtt events, for example with cli mosquitto client:

````
sudo apt-get install mosquitto-clients
mosquitto_sub -h ip_or_hostname -p 1883 -d -t faces/found
````

* Example for MQTT notification of face found:

````
Client mosqsub/7452-ionescu-X5 received PUBLISH (d0, q0, r0, m0, 'faces', ... (100 bytes))
{"type": "face-found", "data": {"image" : "..encoded image", "user_id": "25", "user_name": "Cicilan", bottom_px": 121, "right_px": 237, "top_px": 47, "left_px": 162}
````

To decode the image (in python) use base64.b64decode(data['data']['image'].encode('utf-8'))

Will receive a json encoded user data (if found), and face coordonates in picture


**Troubleshooting:**

* If your're using a raspberry pi and if the camera module is not working please check [this](https://thepihut.com/blogs/raspberry-pi-tutorials/16021420-how-to-install-use-the-raspberry-pi-camera) official Raspberry pi tutorial first

* I've used opencv to capture the camera image from /dev/video0 so ensure it exists, if not you can try to activate it using:

````
sudo modprobe bcm2835-v4l2
````





#Person monitor


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