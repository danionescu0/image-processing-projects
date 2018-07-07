#image is resized by width before processing to increase performance (speed)
resize_image_by_width = 800

# angle to rotate camera in degreeds
rotate_camera_by = 0

# black threshold below level for pupil detecton
pupil_black_level = 70

screen = (1600, 1200)

# mqtt connection details
mqtt = {
    'host' : '192.168.0.111',
    'port' : 1883, # mosquitto default port
    'user' : 'user',
    'password' : 'your_password'
}