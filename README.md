# MS8607
This Python module contains the class that encapsulates basic methods to work with the MS8607 temperature-pressure-humidity sensor board.
The MS8607 board connects to your Raspberry Pi via I2C interface. For Raspberry Pi models A+/B+/2B/3B/3B+/3A+/Zero I2C interface is implemented on the following GPIO pins:
- GPIO PIN #4     5V power    GROVE wire color: RED
- GPIO PIN #6     Ground      GROVE wire color: BLACK
- GPIO PIN #3     I2C SDA     GROVE wire color: WHITE
- GPIO PIN #5     I2C SCL     GROVE wire color: YELLOW

For other Raspberry Pi models please refer to GPIO pinout documentation

To make this Python module work with your Raspberry Pi follow the steps listed below:
1. Activate I2C interface in your OS. In Debian (Raspbian) this can be done with the default configuration utility ```sudo raspi-config```
2. Install pigpio daemon in the OS with ```sudo apt-get install pigpiod``` 
3. Install pigpio module in python with ```pip install pigpio```
4. Run pigpio daemon in the OS with ```sudo pigpiod``` prior to using the MS8607 module in Python
5. Now that you have the daemon running in background, you can import and use the MS8607 module in your Python project ```from MS8607 import MS8607```
