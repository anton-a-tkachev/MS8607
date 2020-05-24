# MS8607 Python module for Raspberry Pi via direct I²C
This Python module contains the class that encapsulates basic methods to communicate with the MS8607 board via direct I²C interface.

The MS8607 is a board equipped with a PHT-sensor (pressure-humidity-temperature) that connects to your Raspberry Pi via direct I²C interface. For Raspberry Pi models A+/B+/2B/3B/3B+/3A+/Zero the I²C interface uses the following GPIO pins:

GPIO PIN | I²C wire |  GROVE wire color
---|---|---
#4 | 5V power | RED
#6 | Ground | BLACK
#3 | SDA | WHITE
#5 | SCL | YELLOW

![Raspberry Pi GPIO pinout diagram](https://github.com/anton-a-tkachev/MS8607/blob/master/GPIO-Pinout-Diagram-2.png "Raspberry Pi GPIO pinout diagram")

For other Raspberry Pi models please refer to GPIO pinout documentation

To make this Python module work with your Raspberry Pi follow the steps listed below:
1. Activate I2C interface in your OS. In Raspbian this can be done with the default configuration utility ```sudo raspi-config```
2. Install pigpio daemon in the OS with ```sudo apt-get install pigpiod``` 
3. Install pigpio module in python with ```pip install pigpio```
4. Run pigpio daemon in the OS with ```sudo pigpiod``` prior to using the MS8607 module in Python
5. Now that you have the daemon running in background, you can import and use the MS8607 module in your Python project ```from MS8607 import MS8607```

Detailed description of pigpio Python module can be found on [pigpio library](http://abyz.me.uk/rpi/pigpio/python.html)

## Basic usage
For a minimal usage example please refer to the file [example.py](https://github.com/anton-a-tkachev/MS8607/blob/master/example.py). 
You can simply run the file with ```python example.py``` from your terminal

## MS8607 list of methods
Here are enumerated the methods to communicate with the MS8607 board via I2C interface in Python

### ```MS8607()``` - constructor
Initializes a connection with the sensors, resets the sensors and fetches conversion coefficients from 0x76 device - temperature and pressure sensor.
The constructor takes two variables:
- I2C bus number (by default ```i2c_bus = 1```)
- pigpio connection handle (by default ```pi = pigpio.pi()```)

When something goes wrong at this stage, there is no exceptions handling, so the user will get a standard error message from python interpreter.

### ```get_t()``` - measure temperature
Attempts to fetch temperature data from the MS8607 board.
Returns a tuple:
- Temperature in degrees Celsius,
- TEMP - auxilary variable used for calculations,
- dT - auxilary variable used for calculations

When unable to fetch the data or any other error, returns ```None``` values.

### ```get_tp()``` - measure temperature and pressure
Returns a tuple:
- Temperature in degrees Celsius,
- Pressure in mbar or hPa (which is the same)

When unable to fetch the data or any other error, returns ```None``` values. Note that the pressure measurement depends on the ambient temperature, so that there is no method for independent pressure measurement.

### ```get_rh()``` - measure relative humidity
Returns relative humidity in %. Temperature reading can be passed to this method for a slightly better accuracy of the relative humidity measurement. If no temperature is passed to the method, then it measures the relative humidity with no correction. 
When unable to fetch the data or any other error, returns ```None```.

### ```get_tph()``` - measure temperature, pressure and humidity
Returns a tuple:
- Temperature in degrees Celsius,
- Pressure in mbar or hPa (which is the same),
- Relative humidity in %

When unable to fetch the data or any other error, returns ```None```.

### ```get_th``` - measure temperature and humidity
Returns a tuple:
- Temperature in degrees Celsius,
- Relative humidity in %

When unable to fetch the data or any other error, returns ```None```.
