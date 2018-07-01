from MathUtils import MathUtils


class RobotSerialCommandsConverter:
    POWER_LIMITS = {'forward' :{'max': 50, 'min': 0}, 'backward': {'max': -50, 'min': 0}}
    DIRECTION_LIMITS = {'right' : 50, 'left' : -50}
    MOTOR_COMMAND = 'M:{0}:{1}'
    MAX_ANGLE = 180
    MIN_ANGLE = 0

    def get_from_eye_mouth(self, eye_horizontal_angle: int, mouth_vertical_percent: int) -> str:
        pass

    def get_steer_command(self, angle: int, percent_power: int, forward: bool) -> str:
        return self.MOTOR_COMMAND.format(
            self.__get_converted_direction(angle),
            self.__get_converted_power(percent_power, forward)
        )

    def __get_converted_power(self, percent_power: int, forward: bool) -> str:
        power_limits_key = {True: 'forward', False: 'backward'}[forward]

        return str(MathUtils.remap(
                percent_power, 0, 100,
                self.POWER_LIMITS[power_limits_key]['min'], self.POWER_LIMITS[power_limits_key]['max']))

    def __get_converted_direction(self, angle: int) -> int:
        return MathUtils.remap(angle, self.MIN_ANGLE, self.MAX_ANGLE,
                               self.DIRECTION_LIMITS['left'], self.DIRECTION_LIMITS['right'])