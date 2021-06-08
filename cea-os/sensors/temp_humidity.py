"""
Hardware
Pin 1 goes to the Pi's 3.3V
Pin 2 goes to GPIO 4
Pin 3 not connected
Pin 4 goes to ground
10 kOhm resistor between data line (GPIO4) and 3.3V

Software
Adafruit Library
Pigpio Library

Instructions for Using Adafruit library:
1. Open up a terminal and make sure you are in your home directory (cd ~)
2. git clone https://github.com/adafruit/Adafruit_Python_DHT.git (clone library)
3. cd Adafruit_Python_DHT (switch into directory you just made)
4. sudo apt-get update (good idea apparently)
5. sudo apt-get install build-essential python-dev (two dependencies needed)
6. sudo python setup.py install (install adafruit software)
7. cd ~ (make sure you are in home directory)
8. /usr/bin/gksu -u root idle (requires goot priveleges to access gpio pins)
9. IDLE should open
10. Code:
import Adafruit_DHT as dht
h, t = dht.read_retry(dht.DHT22, 4) #Polls gpio 4
print 'Temp={0:0.1f}*C Humidity={1:0.1f}%' .format(t, h)
#that's it!

Instructions for Using Pigpio Library
1. cd ~ (make sure you are in your home directory)
2. wget abyz.co.uk/rpi/pigpio/pigpio.zip
3. unzip pigpio.zip
4. cd PIGPIO
5. make
6. make install
7. go to pi gpio website (http://abyz.co.uk/rpi/pigpio/)
8. Click on examples
9. Click on Python Code
10. Find DHT22 Module and click on code to download it
11. We don't need old version so go to Action Extract
12. Go to home directory and create a new folder, call it pigpio_dht22
13. Click Open and selected module will be extracted there
14. Open a terminal and run sudo pigpiod (starts pigpiod daemon)
15. Open up idle as a regular user
16. Code:
import os
os.chdir('pigpio_dht22') #so that new module is in the right path
import pigpio
pi = pigpio.pi()
import DHT22
s = DHT22.sensor(pi, 4) #instantiates sensor connected to gpio4
s.trigger()
print('{:3.2f}'.format(s.humidity() / 1.))
print('{:3.2f}'.format(s.temperature() / 1.))
#that's it!
#side note, s.cancel() will cancel previous instantiation of sensor
#when you are done make sure to call s.cancel() and pi.stop()
# I think we should use the Pigpio option since it doesn't require root priveledge

"""
import os
os.chdir('pigpio_dht22') #so that new module is in the right path
import pigpio
import DHT22
from sensor_definition import Sensor

class TempHumiditySensor(Sensor):
	def __init__(self, gpio=4):
		self.gpio = gpio
		self.pi = pigpio.pi()
		self.s = DHT22.sensor(self.pi, self.gpio)

	def read_value(self):
		self.s.trigger()
		#print('{:3.2f}'.format(s.humidity() / 1.))
		#print('{:3.2f}'.format(s.temperature() / 1.))
		return s.humidity(), s.temperature()

	def calibrate(self, calib_val_humidity, calib_val_temperature):
        """
        This method is used to calibrate the sensor.
        """
        humidity, temperature = self.read_value()
        self.calib_humidity = calib_val_humidity - humidity
        self.calib_temperature = calib_val_temperature - temperature
        print("Calibration value humidity: {0}/nSensor value: {1}".format(calib_val_humidity, humidity))
        print("Calibration value humidity: {0}/nSensor value: {1}".format(calib_val_temperature, temperature))
        pass







