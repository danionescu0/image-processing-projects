import json
import tornado

from UserRepository import UserRepository
from imageprocessing.ImageEncoder import ImageEncoder
from imageprocessing.FacePaths import FacePaths


class UsersHandler(tornado.web.RequestHandler):
    LIMIT = 2

    def initialize(self, user_repo: UserRepository, image_encoder: ImageEncoder, face_paths: FacePaths):
        self.__user_repo = user_repo
        self.__image_encoder = image_encoder
        self.__face_paths = face_paths

    def get(self):
        page = int(self.get_argument('page', 1, True))
        users = self.__user_repo.get_users(page * self.LIMIT, self.LIMIT)
        self.write(json.dumps(self.__get_formatted_users(users)))

    def __get_formatted_users(self, users: list) -> list:
        return [
            {
                'id': user.id,
                'name': user.name,
                'image_ids': user.image_ids,
                'images' : self.__get_images(user.image_ids)
             } for user in users]

    # @Todo remove this .jpg hack
    def __get_images(self, image_ids: list) -> list:
        images = []
        for id in image_ids:
            file_path = self.__face_paths.get_low_resolution(id, 'jpg')
            images.append(self.__image_encoder.encode_image_file(file_path))

        return images


