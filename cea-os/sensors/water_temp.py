from UART_Atlas import AtlasUART
from I2C_Atlas import AtlasI2C
from ftdi_Atlas import AtlasFtdi
from sensor_definition import Sensor

def setup_device(interface, mode_specific_info):
    if interface == 'FTDI':
        atlas_device = AtlasFtdi(
            mode_specific_info) #this location field might need to be replaced by serial_device...
    elif interface == 'UART':
        atlas_device = AtlasUART(
            mode_specific_info,
            baudrate=device.baud_rate)
    elif interface == 'I2C':
        atlas_device = AtlasScientificI2C(
            i2c_address=int(str(mode_specific_info), 16),
            i2c_bus=1)
    else:
        print("Unrecognized interface: {}".format(device.interface))
        return
    return atlas_device

def str_is_float(text):

    try:
        if not text:
            return False
        if text.isalpha():
            return False
        float(text)
        return True
    except ValueError:
        return False

#more specic info is important and for now it assumes I2C mode.
class WaterSensor(Sensor, interface="UART", mode_specific_info=98):
    def __init__(self, input_dev):
        self.input_dev = input_dev
        self.interface = interface
        self.mode_specific_info = mode_specific_info
        self.device = None 

        self.initialize_mode()

    def initialize_mode(self):
        try:
            self.device = setup_device(self.interface, self.mode_specific_info)
        except Exception:
            print("Exception while initializing sensor")

        # Throw out first measurement of Atlas Scientific sensor, as it may be prone to error
        self.read_value()

    def read_value(self):
        """ Gets the Atlas PT1000's temperature in Celsius """
        if not self.device.setup:
            print("Input not set up")
            return

        temp = None
        # Read sensor via FTDI or UART
        if self.interface in ['FTDI', 'UART']:
            temp_status, temp_list = self.device.query('R')

            # Find float value in list
            float_value = None
            for each_split in temp_list:
                if str_is_float(each_split):
                    float_value = each_split
                    break

            if 'check probe' in temp_list:
                print('"check probe" returned from sensor')
            elif str_is_float(float_value):
                temp = float(float_value)
                print('Found float value: {val}'.format(val=temp))
            else:
                print('Value or "check probe" not found in list: {val}'.format(val=temp_list))

        # Read sensor via I2C
        elif self.interface == 'I2C':
            temp_status, temp_str = self.device.query('R')
            if temp_status == 'error':
                print("Sensor read unsuccessful: {err}".format(err=temp_str))
            elif temp_status == 'success':
                temp = float(temp_str)

        if temp == -1023:  # Erroneous measurement
            return

        return temp

    def calibrate(self, calib_val):
        """
        This method is used to calibrate the sensor.
        """
        val = self.read_value()
        self.calib = calib_val - val
        print("Calibration value: {0}/nSensor value: {1}".format(calib_val, val))
        pass
