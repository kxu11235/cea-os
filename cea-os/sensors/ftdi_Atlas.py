import time

import pylibftdi
from pylibftdi import Driver
from pylibftdi.device import Device
from pylibftdi.driver import FtdiError

class AtlasFtdi(Device):
	def __init__(self, serial_device, interface = "ftdi"):
        Device.__init__(self, mode='t', device_id=serial_device)

        self.send_cmd("C,0")  # turn off continuous mode
        time.sleep(1)
        self.flush()

        self.setup = True
        self.interface = interface

    def query(self, query_str):
        """ Send command and return reply """
        try:
            self.send_cmd(query_str)
            time.sleep(1.3)
            response = self.read_lines()
            return 'success', response
        except Exception as err:
            print(
                "{cls} raised an exception when initializing: "
                "{err}".format(cls=self.name, err=err))
            return 'error', err

    def read_line(self, size=0):
        """
        taken from the ftdi library and modified to
        use the ezo line separator "\r"
        """
        lsl = len('\r')
        line_buffer = []
        while True:
            next_char = self.read(1)
            if next_char == '' or 0 < size < len(line_buffer):
                break
            line_buffer.append(next_char)
            if (len(line_buffer) >= lsl and
                    line_buffer[-lsl:] == list('\r')):
                break
        return ''.join(line_buffer)

    def read_lines(self):
        """
        also taken from ftdi lib to work with modified readline function
        """
        lines = []
        try:
            while True:
                line = self.read_line()
                if not line:
                    break
                    # self.flush_input()
                lines.append(line)
            return lines

        except FtdiError:
            print("Failed to read from the sensor.")
            return ''

    def send_cmd(self, cmd):
        """
        Send command to the Atlas Sensor.
        Before sending, add Carriage Return at the end of the command.
        :param cmd:
        :return:
        """
        buf = cmd + "\r"  # add carriage return
        try:
            self.write(buf)
            return True
        except FtdiError:
            print("Failed to send command to the sensor.")

        return False


