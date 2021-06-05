import serial
import sys
from serial import SerialException
from serial.serialutil import SerialTimeoutException

sys.path.append("/Users/guptafamily/cea-os/cea-os/sensors")


class AtlasUART(Object):
	def __init__(self, serial_device, interface="UART", buadrate=9600):
		#Interface means something like I2C vs Uart for example
		self.interface = interface 
		self.serial_device = serial_device
		self.setup = False
		self.name = serial_device.replace("/", "_")

		try:
			self.device = serial.Serial(
                port=serial_device,
                baudrate=baudrate,
                timeout=5,
                writeTimeout=5)

			cmd_return = self.send_cmd('C,0')  # Disable continuous measurements

            if cmd_return:
                self.setup = True

        except serial.SerialException as err:
            print(
                "{cls} raised an exception when initializing: "
                "{err}".format(cls=self.name, err=err))
            print('Opening serial')

    def read_line(self):
        
        lsl = len('\r') #may have to change this \r thing
        line_buffer = []
        while True:
            next_char = self.device.read(1)
            if next_char in [b'', b'\r', '']:
                break
            line_buffer.append(next_char)
            if (len(line_buffer) >= lsl and
                    line_buffer[-lsl:] == list('\r')):
                break
        return b''.join(line_buffer)

    def read_lines(self):
        """
        also taken from ftdi lib to work with modified readline function
        """
        lines = []
        try:
            while True:
                line = self.read_line().decode()
                if not line:
                    break
                    # self.atlas_device.flush_input()
                lines.append(line)
            return lines
        except SerialException:
            print('Exception: Read Lines')
            return None
        except AttributeError:
            print('UART device not initialized')
            return None

	def query(self, query_str): 
        """ Send command and return reply """
        self.send_cmd(query_str)
        time.sleep(1.3)
        response = self.read_lines()
        return 'success', response

        #return None, None

    def write(self, cmd):
        self.send_cmd(cmd)

    def send_cmd(self, cmd):
        """
        Send command to the Atlas Sensor.
        Before sending, add Carriage Return at the end of the command.
        :param cmd:
        :return:
        """
        buf = "{cmd}\r".format(cmd=cmd)  # add carriage return
        try:
            self.device.write(buf.encode())
            return True
        except SerialTimeoutException:
            print("SerialTimeoutException: Write timeout. This indicates "
                              "you may not have the correct device configured.")
        except SerialException:
            print('Send CMD')
            return None
        except AttributeError:
            print('UART device not initialized')
            return None