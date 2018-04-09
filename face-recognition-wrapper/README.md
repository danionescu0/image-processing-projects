# Face recognition wrapper

[Work in progress]

This library is a wrapper for face recognition alorithm.

It provides an http API for:

- creating a person profile

- uploading a photo for the person

- delete a photo for the person

- delete the person


It exposes known and unknown face detections over MQTT.

#### Libraries used (special thanks)

[Opencv](https://github.com/opencv)
[Face recognition](https://github.com/ageitgey/face_recognition)
[Imutils](https://github.com/jrosebr1/imutils)


### Installing dependencies

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

* Create new user


### Listen to mqtt events, for example with cli mosquitto client:

````
sudo apt-get install mosquitto-clients
mosquitto_sub -h ip_or_hostname -p 1883 -d -t faces/found
````

* Example response:

````
Client mosqsub/7452-ionescu-X5 received PUBLISH (d0, q0, r0, m0, 'faces/found', ... (100 bytes))
{"left_px": 187, "user_id": 2, "top_px": 14, "user_name": "dan, "right_px": 262, "bottom_px": 88}
````

Will receive a json encoded user data (if found), and face coordonates in picture