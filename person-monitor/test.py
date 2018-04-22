import time
from lock.TimedLock import TimedLock

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


lock = TimedLock()
print ('set lock cici for 2 seconds')
lock.set_lock("cici", 2)
print ("get lock mim")
print (lock.has_lock("mimi"))
time.sleep(1)
print("after 1 second")
print (lock.has_lock("cici"))
print("after another 1.5 seconds")
time.sleep(1.5)
print (lock.has_lock("cici"))