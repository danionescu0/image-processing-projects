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

    def get_motion_box(self, image):
        (_, initial_width) = image.shape[:2]
        frame = imutils.resize(image, width=self.__resize_width)
        fgmask = self.__background_substraction.apply(frame)
        thresh = cv2.threshold(fgmask, 40, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=3)
        contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not len(contours[1]):
            return None
        contours = [contour for contour in contours[1] if
                    cv2.contourArea(contour) > self.__min_contour_area]
        if len(contours) == 0:
            return None
        x1, x2, y1, y2 = 5000, 5000, 5000, 5000
        for countour in contours:
            (x, y, w, h) = cv2.boundingRect(countour)
            x1 = min(x, x1)
            y1 = min(y, y1)
            x2 = min(x + w, x2)
            y2 = min(y + h, y2)
        if x1 is 5000:
            return None
        (p1x, p1y), (p2x, p2y) = self.__coordonates_scaler\
            .get_scaled(((x1, y1), (x2, y2)), initial_width, self.__resize_width)

        return image[p1y:p2y, p1x:p2x]

