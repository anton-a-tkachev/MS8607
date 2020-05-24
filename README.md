# MS8607
This Python module contains the class that encapsulates basic methods to work with the MS8607 temperature-pressure-humidity sensor board.
The MS8607 board connects to your Raspberry Pi via I2C interface. For Raspberry Pi models A+/B+/2B/3B/3B+/3A+/Zero I2C interface is implemented on the following GPIO pins

GPIO PIN | I2C wire |  GROVE wire color
---|---|---
#4 | 5V power | RED
#6 | Ground | BLACK
#3 | SDA | WHITE
#5 | SCL | YELLOW

For other Raspberry Pi models please refer to GPIO pinout documentation

To make this Python module work with your Raspberry Pi follow the steps listed below:
1. Activate I2C interface in your OS. In Debian (Raspbian) this can be done with the default configuration utility ```sudo raspi-config```
2. Install pigpio daemon in the OS with ```sudo apt-get install pigpiod``` 
3. Install pigpio module in python with ```pip install pigpio```
4. Run pigpio daemon in the OS with ```sudo pigpiod``` prior to using the MS8607 module in Python
5. Now that you have the daemon running in background, you can import and use the MS8607 module in your Python project ```from MS8607 import MS8607```

Detailed documentation of pigpio Python module can be found on [pigpio library](http://abyz.me.uk/rpi/pigpio/python.html)

## MS8607 class methods
### MS8607() - constructor
Initializes connection with the sensors, resets the sensors and fetches conversion coefficients from 0x76 - temperature and pressure sensor. The constructor takes two variables:
- I2C bus number (by default ```i2c_bus = 1```)
- pigpio connection handle (by default ```pi = pigpio.pi()```)
If something goes wrong at this stage, there is no exceptions handling, so the user will get a standard error message from python interpreter.

### get_t() - get temperature
Attempts to fetch temperature data from the MS8607 board. Returns a tuple:
- Temperature in degrees Celsius,
- TEMP - auxilary variable used for calculations,
- dT - auxilary variable used for calculations
If unable to fetch the data or any other error, returns None values.

### get_tp() - get temperature and pressure
Returns a tuple:
- Temperature in degrees Celsius,
- Pressure in mbar or hPa (which is the same)
If unable to fetch the data or any other error, returns None values. Note that the pressure measurement depends on the ambient temperature, so that there is no method for independent pressure measurement.
