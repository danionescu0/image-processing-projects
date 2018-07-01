# Eye mouth remote controll

*Work in progress*


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