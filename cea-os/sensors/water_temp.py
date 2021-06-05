import copy
from UART_Atlas import AtlasUART
from I2C_Atlas import AtlasI2C
from ftdi_Atlas import AtlasFtdi
from sensor_definition import Sensor

def setup_atlas_device(device):
    if device.interface == 'FTDI':
        atlas_device = AtlasFtdi(
            device.ftdi_location) #this location field might need to be replaced by serial_device...
    elif device.interface == 'UART':
        atlas_device = AtlasUART(
            device.uart_location,
            baudrate=device.baud_rate)
    elif device.interface == 'I2C':
        atlas_device = AtlasScientificI2C(
            i2c_address=int(str(device.i2c_location), 16),
            i2c_bus=adevice.i2c_bus)
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

class WaterSensor(Sensor):
    raise NotImplementedError