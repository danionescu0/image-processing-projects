from MathUtils import MathUtils
import cv2

image = cv2.imread("/home/ionescu/projects/python/image-processing-projects/eye-mouth-remote-controll/steering_wheel.png")
cv2.imshow("original", image)
print(image)
cropped = image[70:170, 440:540]
cv2.imshow("cropped", cropped)
cv2.waitKey(0)