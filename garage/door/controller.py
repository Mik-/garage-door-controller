from rpi_driver import RPiDriver
from model import Door
import logging

logging.basicConfig(filename="garagedoor.log",level=logging.DEBUG)

driver = RPiDriver(18, 17, 27)
model = Door("door 1", driver, 5, 1)

while True:
    pass
