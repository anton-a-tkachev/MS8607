"""This demonstrates a minimal usage example"""

from MS8607 import MS8607

sensor = MS8607()

print(sensor.get_t())      # get temperature (with two auxilary variables)
print(sensor.get_rh())     # get humidity
print(sensor.get_tp())     # get temperature and pressure
print(sensor.get_th())     # get temperature and humidity
print(sensor.get_tph())    # get temperature, pressure and humidity
