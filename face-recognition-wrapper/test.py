import cv2

from model.Face import Face
from model.User import User
from UserRepository import UserRepository
import config

repo = UserRepository(config.mongodb_uri)
# repo.add_user(User("1", "july"))
# repo.add_face("4343", "1")
#
# repo.add_user(User("2", "dan"))
# repo.add_face("54645", "2")
#
# repo.add_user(User("3", "alex"))
# repo.add_face("435345", "3")
#
# repo.add_user(User("3", "alex"))
# repo.add_face("435345", "3")
#
# repo.add_user(User("4", "diana"))
# repo.add_face("4574345", "4")
#
# print(repo.get_user('4574345'))

image = cv2.imread("./temp/dan.jpg")
cropped = image[70:170, 440:540]
cv2.imwrite("./temp/dan.jpg", cropped)