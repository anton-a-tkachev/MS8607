"""This demonstrates a minimal usage example"""

from MS8607 import MS8607

pht = MS8607()

print(pht.get_t())      # get temperature (with two auxilary variables)
print(pht.get_rh())     # get humidity
print(pht.get_tp())     # get temperature and pressure
print(pht.get_th())     # get temperature and humidity
print(pht.get_tph())    # get temperature, pressure and humidity
