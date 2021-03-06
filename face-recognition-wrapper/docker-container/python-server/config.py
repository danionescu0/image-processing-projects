image = {
    # image is resized by width before processing to increase performance
    # smaller resolutions means faster detection but lower accuracy
    'resize_image_by_width': 400,

    # angle to rotate camera in degreeds
    'rotate_camera_by': 180,

    # use only a specified percent of the image (starting with the center)
    'use_percent_of_image': 100
}

# number of threads that will be spawned and that will handle actual face detection
# the maximum number of threads you can use is the total available cores on your sistem -1 (the current working thread)
# the more threads you use the more load you'll have on your machine causing more heat on the CPU
frame_processing_threads = 2

# MQTT configuration
# to configure mqtt over websockets: http://www.steves-internet-guide.com/mqtt-websockets/
mqtt = {
    'host': 'mosquitto',
    'port': 1884,
    'user': 'username',
    'password': 'password',
}

# folder containing faces images
faces_path = '/root/image-processing-projects/face-recognition-wrapper/faces/'

mongodb_uri = 'mongodb://mongodb:27017/'