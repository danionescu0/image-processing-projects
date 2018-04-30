import os
import base64
import argparse


import config
from UserRepository import UserRepository

file_path = '/home/ionescu/Downloads/alex.jpg'

with open(file_path, 'rb') as open_file:
    encoded = base64.b64encode(open_file.read()).decode('utf-8')
    print(type(encoded))

    print(type(encoded.encode_numpy_image('utf-8')))

