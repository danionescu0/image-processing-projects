from MathUtils import MathUtils

pupil_center = (32,15)
from_low = 30
from_high = 12
eyes_horizontal_angle = MathUtils.remap(pupil_center[0], from_low, from_high, 0, 180)

print(eyes_horizontal_angle)
