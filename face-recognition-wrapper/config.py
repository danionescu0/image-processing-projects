#image is resized by width before processing to increase performance (speed)
resize_image_by_width = 400

# angle to rotate camera in degreeds
rotate_camera_by = 180

#delay between processing frames, frames are skipped for better performance
process_image_delay_ms = 100

mqtt = {
    'host' : 'localhost',
    'port' : 1883, # mosquitto default port
    'user' : 'user',
    'password' : 'your_password'
}

mongodb_uri = 'mongodb://localhost:27017/'