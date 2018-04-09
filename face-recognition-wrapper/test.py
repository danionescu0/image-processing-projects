from model.Face import Face
from model.User import User
from UserRepository import UserRepository
import config

repo = UserRepository(config.mongodb_uri)
repo.add_user(User("1", "july"))
repo.add_face("4343", "1")

repo.add_user(User("2", "dan"))
repo.add_face("54645", "2")

print(repo.get_user('54645'))