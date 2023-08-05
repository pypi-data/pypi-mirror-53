from octoliner import Octoliner
import time


# Create an object for working with 8-channel line sensor.
octo = Octoliner()
# Set the sensitivity of the photodetectors.
octo.set_sensitivity(1.0)
# Set the brightness of the IR LEDs.
octo.set_brightness(1.0)


def main():
    try:
        while True:
            # List for storing data values from line sensors.
            data_from_sensors = []
            # Read the values from the line sensors and
            # add them to data_from_sensors list.
            for i in range(8):
                data_from_sensors.append(octo.analog_read(i))
            # Print the current line position in the console.
            print(octo.map_line(data_from_sensors))
            # Wait 0.5 seconds.
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
