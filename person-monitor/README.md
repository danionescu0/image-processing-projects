# Person monitor

[work in progress]

In this project we're going to implement a real time person monitor with email notification,
text to speech etc.

We're going to receive face notification from "Face recognition wrapper" over MQTT and react
to them by:

- sending email with known/unknown person 

- use a text to speech API to communicate by voice 

- track known persons on a graph using free IOT platforms like thinger.io

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

* Configure mosquitto user and password and edit config.py and set the mosquitto user and password


