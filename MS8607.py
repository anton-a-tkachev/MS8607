from pigpio import pi
from time import sleep

class MS8607:
    """This Python module contains the class that encapsulates basic methods to work with the MS8607 temperature-pressure-humidity sensor board.

    The MS8607 board connects to your Raspberry Pi via I2C interface. For Raspberry Pi models A+/B+/2B/3B/3B+/3A+/Zero I2C interface is implemented on the following GPIO pins:
        GPIO PIN #4     5V power    GROVE wire color: RED
        GPIO PIN #6     Ground      GROVE wire color: BLACK
        GPIO PIN #3     I2C SDA     GROVE wire color: WHITE
        GPIO PIN #5     I2C SCL     GROVE wire color: YELLOW
    For other Raspberry Pi models please refer to GPIO pinout documentation

    To make this Python module work with your Raspberry Pi follow the steps listed below:
        0. Activate I2C interface in your OS. In Debian (Raspbian) this can be done with the default configuration utility <sudo raspi-config>
        1. Install pigpio daemon in the OS with <sudo apt-get install pigpiod> 
        2. Install pigpio module in python with <pip install pigpio>
        3. Run pigpio daemon in the OS with <sudo pigpiod> prior to using the MS8607 module in Python
        4. Now that you have the daemon running in background, you can import and use the MS8607 module in your Python project    
    """

    def __init__(self, i2c_bus=1, pi=pi()):
        """Initializes connection with the sensors, resets the sensors and fetches conversion coefficients from 0x76 - temperature and pressure sensor.
        When something goes wrong at this stage, there is no exceptions handling, so the user will get a standard error message from python interpreter."""
        self.pi = pi
        self._0x76 = self.pi.i2c_open(i2c_bus=i2c_bus, i2c_address=0x76)    # T and P sensor
        self.pi.i2c_write_device(self._0x76, [0x1E])    # send reset command to 0x76       

        # Read conversion coefficients from 0x76
        self.C = []
        for cmd in range(0xA2, 0xAE, 2):
            self.pi.i2c_write_device(self._0x76, [cmd])
            word = self.pi.i2c_read_device(self._0x76, 2)[1]
            self.C.append(word[0]<<8 | word[1])
        pass

        self._0x40 = self.pi.i2c_open(i2c_bus=i2c_bus, i2c_address=0x40)    # RH sensor
        self.pi.i2c_write_device(self._0x40, [0xFE])    # send reset command to 0x40
    pass

    def get_t(self):
        """Attempts to fetch temperature data from the MS8607 board. Returns a tuple:
        (
            Temperature in degrees Celsius,
            TEMP - auxilary variable used for calculations,
            dT - auxilary variable used for calculations
        )
        When unable to fetch the data or any other error, returns None values."""
        try:
            self.pi.i2c_write_device(self._0x76, [0x5A])
            sleep(0.030)
            word = self.pi.i2c_read_i2c_block_data(self._0x76, 0x00, 3)[1]
            D2 = word[0]<<16 | word[1]<<8 | word[2]
        except:
            return None, None, None
        
        dT = D2 - self.C[4]*2**8
        TEMP = 2000 + dT*self.C[5]/2**23
        T = TEMP/100.0
        return T, TEMP, dT
    pass

    def get_tp(self):
        """Returns a tuple:
        (
            Temperature in degrees Celsius,
            Pressure in mbar or hPa (which is the same)
        )
        When unable to fetch the data or any other error, returns None values.
        Note that the pressure measurement depends on the ambient temperature, so that there is no method for independent pressure measurement.
        """
        T, TEMP, dT = self.get_t()
        if T == None or TEMP == None or dT == None:
            return None, None

        try:
            self.pi.i2c_write_device(self._0x76, [0x4A])
            sleep(0.030)
            word = self.pi.i2c_read_i2c_block_data(self._0x76, 0x00, 3)[1]
            D1 = word[0]<<16 | word[1]<<8 | word[2]
        except:
            return T, None

        OFF = self.C[1]*2**17 + self.C[3]*dT/2**6
        SENS = self.C[0]*2**16 + self.C[2]*dT/2**7
        if TEMP < 2000:
            T2 = 3*dT**2/2**33
            OFF2 = 61*(TEMP - 2000)**2/2**4
            SENS2 = 29*(TEMP - 2000)**2/2**4
            if TEMP < -1500:
                OFF2 = OFF2 + 17*(TEMP + 1500)**2
                SENS2 = SENS2 + 9*(TEMP + 1500)**2
        else:
            T2 = 5*dT**2/2**38
            OFF2 = 0
            SENS2 = 0

        TEMP = TEMP - T2
        OFF = OFF - OFF2
        SENS = SENS - SENS2

        P = (D1*SENS/2**21 - OFF)/2**15/100.0

        return T, P
    pass

    def get_rh(self, T = 20.0):
        """Returns relative humidity in %. Temperature reading can be passed to this method for a slightly better accuracy of the relative humidity measurement. If no temperature is passed to the method, then it measures the relative humidity with no correction.
        When unable to fetch the data or any other error, returns None."""
        try:
            self.pi.i2c_write_device(self._0x40, [0xE5])
            word = self.pi.i2c_read_device(self._0x40, 2)[1]
            D3 = word[0] << 8 | word[1]
        except: 
            return None

        RH = -6.0 + 125.0*D3/2**16
        if T != None: RH = RH + 0.18*(T - 20.0)
        return RH
    pass

    def get_tph(self):
        """Returns a tuple:
        (
            Temperature in degrees Celsius,
            Pressure in mbar or hPa (which is the same),
            Relative humidity in %
        )
        When unable to fetch the data or any other error, returns None.
        """
        T, P = self.get_tp()
        RH = self.get_rh(T)
        return T, P, RH
    pass 

    def get_th(self):
        """Returns a tuple:
        (
            Temperature in degrees Celsius,
            Relative humidity in %
        )
        When unable to fetch the data or any other error, returns None.
        """
        T = self.get_t()[0]
        RH = self.get_rh(T)
        return T, RH
    pass
pass
