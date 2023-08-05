from .gpioexp import gpioexp
from .gpioexp import GPIO_EXPANDER_DEFAULT_I2C_ADDRESS as DFLT_ADDR


class Octoliner(gpioexp):
    """
    Class for 8-channel Line sensor.

    Methods:
    --------
    set_sensitivity(sense: float) -> None
        Set the sensitivity of the photodetectors in the range
        from 0 to 1.0.

    set_brightness(brightness: float) -> None
        Set the brightness of the IR LEDs in the range
        from 0 to 1.0.

    analog_read(sensor: float) -> float
        Read the value from one line sensor.
        Return value in range from 0 to 1.0.

    map_line(binary_line: list) -> float
        Convert data from sensors to the relative position of the line.
        The return value in the range from -1.0 to 1.0.

    """

    def __init__(self, i2c_address=DFLT_ADDR):
        """
        The constructor for Octoliner class.

        Parameters:
        -----------
        i2c_address: int
            Board address on I2C bus (default is 42).
        """
        super().__init__(i2c_address)
        self._led_brightness_pin = 9
        self._sense_pin = 0
        self._sensor_pin_map = (4, 5, 6, 8, 7, 3, 2, 1)
        self._value = 0

    def set_sensitivity(self, sense):
        """
        Set the sensitivity of the photodetectors in the range
        from 0 to 1.0.

        Parameters:
        -----------
        sense: float
            Sensitivity of the photodetectors in the range
            from 0 to 1.0.
        """
        self.analogWrite(self._sense_pin, sense)

    def set_brightness(self, brightness):
        """
        Set the brightness of the IR LEDs in the range
        from 0 to 1.0.

        Parameters
        ----------
        brightness: float
            Brightness of the IR LEDs in the range
            from 0 to 1.0.
        """
        self.analogWrite(self._led_brightness_pin, brightness)

    def analog_read(self, sensor):
        """
        Read the value from one line sensor.
        Return value in range from 0 to 1.0.

        Parameters:
        -----------
        sensor: int
            Pin number to get value from.
        """
        sensor &= 0x07
        return self.analogRead(self._sensor_pin_map[sensor])

    def map_line(self, binary_line):
        """
        Convert data from sensors to the relative position of the line.
        The return value in the range from -1.0 to 1.0:
            – "-1.0" corresponds to the leftmost position of the sensor.
            – "1.0" corresponds to the rightmost position of the sensor.
            – "0.0" – the sensor is in the middle of the line.

        Parameters:
        -----------
        binary_line: list
            List of data values from line sensors.
        """
        pattern = 0
        # Search min and max values in binary_line list.
        min_val = float("inf")
        max_val = 0
        for val in binary_line:
            if val < min_val:
                min_val = val
            if val > max_val:
                max_val = val
        threshold = min_val + (max_val - min_val) / 2
        for val in binary_line:
            pattern = (pattern << 1) + (0 if val < threshold else 1)
        self._value = self._check_pattern(pattern)
        return self._value

    def _check_pattern(self, pattern):
        """
        Return pattern from line sensors patterns dictionary.

        Parameters:
        -----------
        pattern: int
            Combination of data from line sensors.
        """
        patterns_dict = {
            0b00011000: 0,
            0b00010000: 0.25,
            0b00111000: 0.25,
            0b00001000: -0.25,
            0b00011100: -0.25,
            0b00110000: 0.375,
            0b00001100: -0.375,
            0b00100000: 0.5,
            0b01110000: 0.5,
            0b00000100: -0.5,
            0b00001110: -0.5,
            0b01100000: 0.625,
            0b11100000: 0.625,
            0b00000110: -0.625,
            0b00000111: -0.625,
            0b01000000: 0.75,
            0b11110000: 0.75,
            0b00000010: -0.75,
            0b00001111: -0.75,
            0b11000000: 0.875,
            0b00000011: -0.875,
            0b10000000: 1.0,
            0b00000001: -1.0,
        }
        # If pattern key exists in patterns_dict return it,
        # else return current self._value.
        return patterns_dict.get(pattern, self._value)
