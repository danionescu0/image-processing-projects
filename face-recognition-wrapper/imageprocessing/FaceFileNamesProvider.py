import os
from typing import List


class FaceFileNamesProvider:
    __EXCLUDE = ['_temp', '_thumb', 'gitignore']

    def load(self, path: str) -> List[str]:
        faces = []
        for root, subdirs, files in os.walk(path):
            for file in os.listdir(root):
                filePath = os.path.join(root, file)
                if os.path.isdir(filePath):
                    continue
                if any(exc in filePath for exc in self.__EXCLUDE):
                    continue
                faces.append(filePath)

        return faces