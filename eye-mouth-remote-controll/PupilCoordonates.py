import cv2


class ColoredObjectDetector:
    def find_pupil(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY_INV)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        cv2.imshow("computer vision", thresh)
        contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]

        if len(contours) == 0:
            return (False, False)
        largest_contour = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)
        M = cv2.moments(largest_contour)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        return (center, int(radius))