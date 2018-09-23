import cv2
import numpy as np


class FaceDetector:
    def __init__(self, prototext_path: str, model_path: str, min_confidence: int) -> None:
        self.__prototext_path = prototext_path
        self.__model_path = model_path
        self.__min_confidence = min_confidence
        self.__net = None

    def configure(self):
        self.__net = cv2.dnn.readNetFromCaffe(self.__prototext_path, self.__model_path)

    def find(self, image):
        (h, w) = image.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
        # pass the blob through the network and obtain the detections and predictions
        self.__net.setInput(blob)
        detections = self.__net.forward()
        # loop over the detections
        valid_detections = []
        for i in range(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with the prediction
            confidence = detections[0, 0, i, 2]
            # filter out weak detections
            if confidence < self.__min_confidence:
                continue
            # compute the (x, y)-coordinates of the bounding box for the object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box
            valid_detections.append((int(startY), int(endX), int(endY), int(startX)))

        return valid_detections