# Face recognition wrapper

This library uses a video stream (from a webcam or raspbery pi camera) to identify faces and match then against 
known persons and notify what has found over MQTT.

* Features
* Installing with docker-compose
* Manually installing dependencies, configure and run the project
* CRUD operations
* Troubleshooting
* How does it work

### Features:

- face identification in video stream

- face matching against known persons faces

- it uses a configurable number of processes to make use of all the cores in the system 

- HTTP API to create, add delete user and faces

- MQTT notifications with face coordonates, person id (if found), and encoded image


The library is suited for a development board like Raspberry pi and for a face tracking and face recognition.

![diagram.png](https://github.com/danionescu0/image-processing-projects/blob/master/media/diagram.png)

### Installing with docker-compose
1. Install docker and docker compose
  
docker: curl -sSL https://get.docker.com | sh
docker compose: https://medium.freecodecamp.org/the-easy-way-to-set-up-docker-on-a-raspberry-pi-7d24ced073ef

2. Clone project:
````
git clone https://github.com/danionescu0/image-processing-projects
````
3. Go to docker folder:
````
cd image-processing-projects/face-recognition-wrapper
````

4. Configurations:
 
Edit ./moquitto/Dockerfile and change the default username and password

Edit ./python-server/config.py and configure mosquitto username, password, and change any parameters if needed


5. Ensure /dev/video0 is available on the machine

If not try to connect a USB camera, or if you're using a Raspberry PI with the pi camera try the commad:
````
sudo modprobe bcm2835-v4l2
````
This will mount /dev/video0

If your video source is other than /dev/vide0 you'll need to change:
- ./python-server/Dockerfile and replace

````
CMD ["python3", "video_processor.py", "--camera_device", "0"]
````

0 with whatever your camera is mounted on ex: /dev/video2 will mean "2".

- ./docker-compose.yml and replace /dev/video0 with whatever you have

5. Build the containers
````
docker-compose build
````

6. Run the containers

````
docker-compose up
````

7. (Optional) Use CURL to create a list of profiles. You can find the CRUD request description below

8. (Optional) Configure port forwarding in your router to access the resources from the internet 
  Warning this is not secured yet
 
9. Receive notification of persons (maybe use person-monitor project)

10. (Optional) to run this as a service on system start on raspberry pi

a. Copy the files from systemctl folder in systemctl folder to /etc/systemd/system/

b. Enable services:
````
sudo systemctl enable rpi-docker-startup.service
````

c. Reboot

d. Optional, check status:
````
sudo systemctl status rpi-docker-startup.service
````


### Manually installing dependencies, configure and run the project

* Edit config.py and configure MQTT, and other settings if needed

* Install python requirements:
````
pip install -r requirements.txt
````

* Install mongodb 
````
sudo apt-get install mongodb
````

* Mosquitto MQTT broker: https://mosquitto.org/download/

````
sudo apt-get install mosquitto
````

* Configure mosquitto user and password and edit config.py and set the mosquitto user and password

For more information on how to set user and password check this url: http://www.steves-internet-guide.com/mqtt-username-password-example/


* Start the web server
````
python webserver.py 
````

* Start the background process

````
python video_processor.py --camera_device 0
````
0 means it's mapped with /dev/video0.


to start the video in debug mode (display the video source in a window)
````
python video_processor.py --show-video --camera_device 0 
````

### CRUD operations

HTTP API:

- create a person profile

- upload a photo for the person

- delete a person photo

- get persons data

**Create new user**

POST request to: machine_ip:8080/user/userid

GET parameters: userid

POST parameters: "name" containing the user name

````
curl -X POST -d name=some_name http://machine_ip:8080/user/some_numeric_id
````

**Add new face to user**

POST request to: http://machine_ip:8080/face/face_id

GET parameters: "face_id": id of the face that will be stored in the db

POST parameters: "user_id": to what user id does the face belongs; "photo": the file to be upladed (containing one face)

````
curl -F "user_id=1" -F "photo=@/path_to_picture/picture.jpg" http://machine_ip:8080/face/face_number
````

**Delete face for user**

DELETE request to: http://machine_ip:8080/face/face_id

GET parameters: "face_id": id of the face that will be stored in the db

````
curl -X DELETE http://machine_ip:8080/face/1
````

**Get users with photos**

Get request to: http://machine_ip:8080/users?page=page_number

GET parameters: "page" the page number to be returned

````
curl -i http://machine_ip:8080/users?page=1
````
### Listen to MQTT events, for example with cli mosquitto client:

````
sudo apt-get install mosquitto-clients
mosquitto_sub -h ip_or_hostname -p 1884 -d -t faces

# or with username and password
mosquitto_sub -h ip_or_hostname -u username -P password -p 1884 -d -t faces
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

### How does it work

**How does the whole mechanism is put togeather from getting the frames through the camera to sending faces and coordonates through MQTT ?**

The main program runs in an infinite loop until "q" key is pressed and performs series of steps:

1. reads a frame from the camera using opencv camera api
2. rotates the camera if needed (there is a good change that the camera is mounted upside down or at an arbitrary angle)
3. searches for motion in the frames, if found it returns a rectangle that contain motion
4. if it has found motion, the algorithm continues asyncroniously on several processes that try to detect faces in the image.
5. when a face or faces are detected the asyncronious processes communicates this by putting the images and the faces found on a special queue that can communicate between processes
6. syncroniously still inside the loop the queue is queried for found images and faces
7. if faces are found, image data along with faces coordonates and user data are sent through MQTT

**How do we search for motion**
1. the image is resized in a smaller format like 400x300 for better performance
2. we use opencv function "createBackgroundSubtractorMOG2" to get areas of the images that contain motion
3. using opencv "threshold" function we are able to convert the output of the function above to a mask containing motion or no motion pixels (black and white)
4. we're applying opencv "dilate" function to create the motion zones more smoother and enlarge them a bit
5. using opencv "findContours" we're able to get an array of all found objects that are in motion 
6. the final step loops through all of the countours, discard the small ones, and find a maximum rectangle that fits all remaining objects

**How does the face detection and face recognition works ?**
 
For face detection and face recognition i'm using face_recognition library: https://github.com/ageitgey/face_recognition. 

This library has a 4 step process:

1. load faces that we need to match from disk and encode them
2. find faces in a given image
3. encode the found faces
4. compare the encoded faces with the encodings from those found on disk

Because we're runing on a development board before applying these steps, we need to scale the image to a low resolution so we achieve 
about one frame per second. The scaling is configurable, and the default for a raspberry pi is scale by width by 400

**What is the role of the webserver?**
The webserver manages CRUD operatons for the users: create, get, update, delete, add new face etc.

**How does the background process (video_processor.py) is able to load new faces and delete other without restarting the service**
The background process listens using MQTT to some special events that say "this face has been added" or "that face has been deleted" 
and updates the in memory face detectors

**What is docker role in this project**

Docker along docker-compose will create the infrastructure and configure all dependencies with minimum effort.

There are four containers defined in docker-compose.yml and one for person monitor

1. mongoDb instance container. This will store the users data
2. Mosquitto container. This is the mean of communication for found faces
3. face-tracker container. This will run the video_processor.py command
4. face-tracker-webserver container. This will run the webserver that exposes the CRUD api
5. an optional person-monitor container. This is not related to face-recognition-wrapper. This conainer runs https://github.com/danionescu0/image-processing-projects/tree/master/person-monitor
