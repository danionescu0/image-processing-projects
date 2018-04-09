# Face recognition wrapper

[Work in progress]

This library is a wrapper for "face_recognition".

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
