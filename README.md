#Face recognition wrapper

Video demo: https://www.youtube.com/watch?v=qufa4i4dOds&index=36&list=PLl_Vyjgh2HiI5V5EZHxj4Z3bFgkz9-2Z-&t=5s

This library  uses a video stream (from a webcam or raspbery pi camera) to identify faces and match then against 
known persons and notify what has found using MQTT.

**Full documentation here:** https://github.com/danionescu0/image-processing-projects/tree/master/face-recognition-wrapper

*Features:*

- face identification in video stream

- face matching against known persons faces

- it uses a configurable number of processes to make use of all the cores in the system 

- HTTP API to create, add delete user and faces

- MQTT notifications with face coordonates, person id (if found), and encoded image

The library is well suited for a development board like Raspberry pi and for a face tracking and face recognition.

#Person monitor

In this project we're going to implement a real time person monitor with email notification,
text to speech and DeviceHub integrations using the face recognition wrapper project (above)

**Full documentation here:** https://github.com/danionescu0/image-processing-projects/tree/master/person-monitor

We're going to receive face notification from "Face recognition wrapper" over MQTT and react to them by:

- sending email with known/unknown person along with a picture

- use a text to speech API to communicate by voice 

- track known persons on a graph using free IOT platforms like devicehub

#Eye mouth remote controll](#Eye-mouth-remote-controll

Video demo: https://www.youtube.com/watch?v=qufa4i4dOds&index=36&list=PLl_Vyjgh2HiI5V5EZHxj4Z3bFgkz9-2Z-&t=5s

This project takes a video stream identify the eyes and mouth and enable their coordonates to be used as a remote controll

**Full documentation here:** https://github.com/danionescu0/image-processing-projects/tree/master/eye-mouth-remote-controll

The pupil coordonates will be compared to the eye corners and an angle will be extracted.

0 degreeds for maximum left pupil position, 180 degres for maximum right pupil position.

The mouth opening will me measured, and for maximum opening there will be a value of 100, for minimum opening  a value of 0

My current demo will be to use this repository: https://github.com/danionescu0/robot-camera-platform

to command the robot direction using the eyes and the speed using the mouth.
