from garage.door.model import Door
import web
import logging
from optparse import OptionParser
import sys
import json
import importlib

web.config.debug = False

logger = logging.getLogger('garage')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

filehandler = logging.FileHandler('garage.log')
filehandler.setLevel(logging.DEBUG)
filehandler.setFormatter(formatter)
logger.addHandler(filehandler)

config_filename = 'config.json'
door_list = []

urls = (
    '/doors', 'ListDoors',
    '/door/(.*)', 'DoorState'
)

class ListDoors:
    def GET(self):
        response = '{"doors": ['

        i = 1
        for door in door_list:
            if i <> 1:
                response += ','
            response += '{"id": "%d", "name": "%s"}' % (i, door.name)
            i += 1

        response += ']}'
        return response

class DoorState:
    def GET(self, door_id):
        id = int(door_id)
        response = '{"name": "%s","state": "%s","intent": "%s"}' % (
            door_list[id].name, door_list[id].state.__class__.__name__,
            door_list[id].intent.__class__.__name__)
        return response

    def POST(self, door_id):
        id = int(door_id)

        door_list[id].start_door_signal()

def init():
    # Process config file
    with open(config_filename) as json_data_file:
        config_data = json.load(json_data_file)

    for door_config in config_data["door-list"]:
        if door_config["driver"]["class"] == "MockDriver":
            # Instantiate mock driver
            mockdriver_module = importlib.import_module("tests.mock_driver")
            driver = getattr(mockdriver_module, "MockDriver")()
        elif door_config["driver"]["class"] == "RPiDriver":
            # Instantiate RPi driver
            rpidriver_module = importlib.import_module("garage.door.rpi_driver")
            driver = getattr(rpidriver_module, "RPiDriver")(
                door_config["driver"]["gpioRelay"],
                door_config["driver"]["gpioUpperLimitSwitch"],
                door_config["driver"]["gpioLowerLimitSwitch"])

        new_door = Door(door_config["name"], driver, door_config["transitTime"],
            door_config["triggerTime"], door_config["accelerateTime"])
        door_list.append(new_door)

if __name__ == "__main__":
    # Parse the command line options
    parser = OptionParser()
    parser.add_option("-c", "--config", dest="config_filename", help="config filename; defaults to config.json")
    (options, args) = parser.parse_args()

    if options.config_filename:
        config_filename = options.config_filename

    # args contains the remaining options. Assign args to sys.argv to hand them
    # over to the web app
    sys.argv = args

    init()

    app = web.application(urls, globals())

    app.run()
