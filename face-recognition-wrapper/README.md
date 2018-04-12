# Face recognition wrapper



This library is a wrapper for face recognition alorithm and exposes the following API:

It provides an http API for:

- creating a person profile

- uploading a photo for the person

- delete a photo for the person

- delete the person


It exposes known and unknown face detections over MQTT.

The library is well suited for a development board like Raspberry pi and for a face tracking and recognition projects.

#### Libraries used (special thanks) for image processing

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

POST request to: your_ip:8080/user/userid

parameters:

"name" containing the user name

* Add new face to user

POST request to: your_ip:8080/face/1

parameters:

"user_id": to what user id does the face belongs

"photo": the file to be upladed (containing one face)


### Listen to mqtt events, for example with cli mosquitto client:

````
sudo apt-get install mosquitto-clients
mosquitto_sub -h ip_or_hostname -p 1883 -d -t faces/found
````

* Example for mqtt notification of face found:

````
Client mosqsub/7452-ionescu-X5 received PUBLISH (d0, q0, r0, m0, 'faces', ... (100 bytes))
{"type": "face-found", "data": {"image" : "..encoded image" , "user_name": "Cicilan", "bottom_px": 121, "right_px": 237, "top_px": 47, "user_id": "25", "left_px": 162}
````

To decode the image first use base64.b64decode(data['data']['image'].encode('utf-8'))

Will receive a json encoded user data (if found), and face coordonates in picture


**Troubleshooting:**

* If your're using a raspberry pi and if the camera module is not working please check [this](https://thepihut.com/blogs/raspberry-pi-tutorials/16021420-how-to-install-use-the-raspberry-pi-camera) official Raspberry pi tutorial first

* I've used opencv to capture the camera image from /dev/video0 so ensure it exists, if not you can try to activate it using:

````
sudo modprobe bcm2835-v4l2
````