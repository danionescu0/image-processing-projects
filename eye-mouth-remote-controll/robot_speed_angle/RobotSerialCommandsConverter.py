from MathUtils import MathUtils
from command.Coordonates import Coordonates


class RobotSerialCommandsConverter:
    POWER_LIMITS = {'forward' :{'max': 50, 'min': 0}, 'backward': {'max': -50, 'min': 0}}
    DIRECTION_LIMITS = {'right' : 50, 'left' : -50}
    MOTOR_COMMAND = 'M:{0}:{1}'
    MAX_ANGLE = 180
    MIN_ANGLE = 0

    def get_from_coordonates(self, coordonates: Coordonates) -> str:
        return self.MOTOR_COMMAND.format(
            self.__get_converted_direction(coordonates.eyes_horizontal_angle),
            self.__get_converted_power(coordonates.mouth_vertical_percent, True)
        )

    def __get_converted_power(self, percent_power: int, forward: bool) -> str:
        power_limits_key = {True: 'forward', False: 'backward'}[forward]

        return str(MathUtils.remap(
                percent_power, 0, 100,
                self.POWER_LIMITS[power_limits_key]['min'], self.POWER_LIMITS[power_limits_key]['max']))

    def __get_converted_direction(self, angle: int) -> int:
        return MathUtils.remap(angle, self.MIN_ANGLE, self.MAX_ANGLE,
                               self.DIRECTION_LIMITS['left'], self.DIRECTION_LIMITS['right'])