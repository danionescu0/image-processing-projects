import facebook

graph = facebook.GraphAPI(access_token="EAAEIARXdEpkBANR9Onc0IsZAo6XU7542p1Yez1RB0tKIs1huYZAzoHx8NM7sdcKRLtoAdHGRWTxxN0cPs1QoELGtr9wPd9fUEOkaYq0dczuEdfC7GmxrRnhmE5Vy9OYcXkpw7B7cBQyZAFRSWN9kk07rq6i3SXJoMXyYHTqWwZDZD", version="2.12")

friends = graph.get_connections(id='me', connection_name='phoos')

# photos = graph.get_object("me/feed")
# print(photos)
# for photo in photos['data']:
#     print (photos)

print(friends)