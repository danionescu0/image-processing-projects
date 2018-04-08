import os
from typing import List


class FaceFileNamesProvider:
    def load(self, path: str) -> List[str]:
        faces = []
        for root, subdirs, files in os.walk(path):
            for file in os.listdir(root):
                filePath = os.path.join(root, file)
                if os.path.isdir(filePath):
                    pass
                faces.append(filePath)

        return faces