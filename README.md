Projects:

1. [Face recognition wrapper](#Face-recognition-wrapper)

2. [Person monitor](#Person-monitor)

3. [Eye mouth remote controll](#Eye-mouth-remote-controll)

Video demo: https://www.youtube.com/watch?v=qufa4i4dOds&index=36&list=PLl_Vyjgh2HiI5V5EZHxj4Z3bFgkz9-2Z-&t=5s

# Face recognition wrapper

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

* Install mongodb 
````
sudo apt-get install mongodb
````

* Mosquitto mqtt broker: https://mosquitto.org/download/

````
sudo apt-get install mosquitto
````

* Configure mosquitto user and password and edit config.py and set the mosquitto user and password

For more information on how to set user and password check this url: http://www.steves-internet-guide.com/mqtt-username-password-example/

### Running the project
activate virtual environment if needed

* Start the web server
````
python webserver.py 
````

* Start the background process

````
python video_processor.py --camera_device 0
````
Camera parameter is optional and it's mapped to the camera resource. It can be a raspberry pi camera or a webcam:
0 means it's mapped with /dev/video0.

If you're using a raspberry pi camera and have picamera module installed you can omit the --camera_device parameter, if you're using a webcam you need to specify the device number

to start the video in debug mode (display the video source in a window)
````
python video_processor.py --show-video --camera_device 0 --show-video
````

### Creating users, deleting users, adding faces to users, deleting faces

HTTP API:

- create a person profile

- upload a photo for the person

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
{"type": "face-found", "data": {"image" : "..encoded image", faces: [{"user_id": "25", "user_name": "Cicilan", bottom_px": 121, "right_px": 237, "top_px": 47, "left_px": 162}, ...{..} ]}
````

To decode the image (in python) use base64.b64decode(data['data']['image'].encode('utf-8'))

Will receive a json encoded user data (if found), and face coordonates in picture


**Troubleshooting:**

* If your're using a raspberry pi and if the camera module is not working please check [this](https://thepihut.com/blogs/raspberry-pi-tutorials/16021420-how-to-install-use-the-raspberry-pi-camera) official Raspberry pi tutorial first

* I've used opencv to capture the camera image from /dev/video0 so ensure it exists, if not you can try to activate it using:

````
sudo modprobe bcm2835-v4l2
````




# Person monitor


In this project we're going to implement a real time person monitor with email notification,
text to speech and DeviceHub integrations.

We're going to receive face notification from "Face recognition wrapper" over MQTT and react
to them by:

- sending email with known/unknown person along with a picture

- use a text to speech API to communicate by voice 

- track known persons on a graph using free IOT platforms like devicehub



### Installing dependencies & configure

* Edit config.py and configure mqtt, and other settings if needed

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

# Eye mouth remote controll

Video demo: https://www.youtube.com/watch?v=qufa4i4dOds&index=36&list=PLl_Vyjgh2HiI5V5EZHxj4Z3bFgkz9-2Z-&t=5s

This project takes a video stream identify the eyes and mouth and enable their coordonates to be used as a remote controll

The pupil coordonates will be compared to the eye corners and an angle will be extracted.

0 degreeds for maximum left pupil position, 180 degres for maximum right pupil position.

The mouth opening will me measured, and for maximum opening there will be a value of 100, for minimum opening  a value of 0

My current demo will be to use this repository: https://github.com/danionescu0/robot-camera-platform

to command the robot direction using the eyes and the speed using the mouth.


*Selecting a video camera*
The video camera should meet this criterias:

- it should have night vision

- it should have over 5 MP resoulution

If you want to use a raspberry pi camera on your laptop it cannot be done directly, but you can stream the video using

uv4l (https://www.linux-projects.org/uv4l/installation/) and then use the stream locally using -v option in the python script

ex: -v http://ip:port/stream/video.mjpeg

My tests are made with raspberry pi night vision camera and the results are pretty good.


1. Install python requirements:
````
pip install -r requirements.txt
````

2 . Download Dlib face model 

````
wget https://github.com/davisking/dlib-models/raw/master/shape_predictor_68_face_landmarks.dat.bz2
````

Then unarchive

3. Use the script as follows

````
python3 video_processor.py -p path_to_unarchived_dlib_face_model -v /dev/video0
````

Where /dev/video0 is your webcam or another vide device, or a video recording like mp4

4. Position your face in front of the camera.

The face should occupy 70% of the image height, and the head must be straight

5. Calibrate the eyes, mouth coordonates using arrow keys.

If the face is not in the right position (see above) you will see a "No face" text on the video stream

Look to your maximum right and press right arrow key

Look to your maximum left and press left arrow key

Open your mouth and press up key

Close your mouth and press down key

6. Using the remote

Now the left, right (steer) and stop, start (speed) are calibrated.

While your face is in the correct position the steering wheel will rotate on the screen, 

and the robot commands will be issued through mqtt. For more information please visit: ttps://github.com/danionescu0/robot-camera-platform


## Troubleshoot:

where /dev/video0 is your webcam or another vide device, or a video recording like mp4