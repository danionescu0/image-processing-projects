import cv2
import imutils

from imageprocessing.CoordonatesScaler import CoordonatesScaler


class MotionDetector:
    def __init__(self, coordonates_scaler: CoordonatesScaler, resize_width: int, min_contour_area: int) -> None:
        self.__coordonates_scaler = coordonates_scaler
        self.__resize_width = resize_width
        self.__min_contour_area = min_contour_area

    def configure(self):
        self.__background_substraction = cv2.createBackgroundSubtractorMOG2(history=2)

    # todo improve this algotitm
    def get_motion_box(self, image):
        (_, initial_width) = image.shape[:2]
        frame = imutils.resize(image, width=self.__resize_width)
        fgmask = self.__background_substraction.apply(frame)
        thresh = cv2.threshold(fgmask, 40, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=3)
        countours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        x1 = []
        x2 = []
        y1 = []
        y2 = []
        for c in countours[1]:
            if cv2.contourArea(c) < self.__min_contour_area:
                continue
            (x, y, w, h) = cv2.boundingRect(c)
            x1.append(int(x))
            y1.append(int(y))
            x2.append(int(x + w))
            y2.append(int(y + h))
        if len(x1) > 0:
            (p1x, p1y), (p2x, p2y) = self.__coordonates_scaler\
                .get_scaled(((min(x1), min(y1)), (max(x2), max(y2))), initial_width, self.__resize_width)
            return image[p1y:p2y, p1x:p2x]

        return None