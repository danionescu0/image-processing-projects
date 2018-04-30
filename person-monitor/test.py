import time
from lock.TimedLock import TimedLock
from devicehub.devicehub import Sensor, Actuator, Device, Project
from random import randint
from time import sleep
import requests

# import facebook
#
# graph = facebook.GraphAPI(access_token="EAAEIARXdEpkBANR9Onc0IsZAo6XU7542p1Yez1RB0tKIs1huYZAzoHx8NM7sdcKRLtoAdHGRWTxxN0cPs1QoELGtr9wPd9fUEOkaYq0dczuEdfC7GmxrRnhmE5Vy9OYcXkpw7B7cBQyZAFRSWN9kk07rq6i3SXJoMXyYHTqWwZDZD", version="2.12")
#
# friends = graph.get_connections(id='me', connection_name='phoos')

# photos = graph.get_object("me/feed")
# print(photos)
# for photo in photos['data']:
#     print (photos)

# print(friends)
print(int(time.time()))


#curl -H "X-ApiKey: ed16df23-36e4-4507-94d0-654af8172e58" -H "Content-Type: application/json" -i "https://api.devicehub.net/v2/project/4/device/e62fbb50-9fca-4188-8a3a-92d8452c7e66/sensor/Dan/data" -d "{\"value\":0}"


PROJECT_ID = '4'
DEVICE_UUID = 'e62fbb50-9fca-4188-8a3a-92d8452c7e66'
API_KEY = 'ed16df23-36e4-4507-94d0-654af8172e58'
# project = Project(PROJECT_ID, persistent=True)
# device = Device(project, DEVICE_UUID, API_KEY)
# dan = Sensor(Sensor.ANALOG, 'Dan')
# device.addSensor(dan)
#
#
# dan.addValue(1)
# sleep(5)
# device.send()
headers = {
    'X-ApiKey' : 'ed16df23-36e4-4507-94d0-654af8172e58',
    'Content-Type': 'application/json'
}
r = requests.post("https://api.devicehub.net/v2/project/4/device/e62fbb50-9fca-4188-8a3a-92d8452c7e66/sensor/Dan/data",
                  headers=headers,
                  data='{\"value\":1}')
print(r.status_code, r.reason)