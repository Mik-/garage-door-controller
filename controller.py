from garage.door.rpi_driver import RPiDriver
#from tests.mock_driver import MockDriver
from garage.door.model import Door
import web
import logging

logger = logging.getLogger('garage')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

filehandler = logging.FileHandler('garage.log')
filehandler.setLevel(logging.DEBUG)
filehandler.setFormatter(formatter)
logger.addHandler(filehandler)

# create the door_list only once, web.py loads this module at least twice
if web.config.get('_door_list') is None:
    driver = RPiDriver(18, 17, 27)
    #driver = MockDriver()

    door_list = []
    door_list.append(Door("door 1", driver, 5, 1, 2))
    web.config._door_list = door_list
else:
    door_list = web.config._door_list

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


if __name__ == "__main__":
    app = web.application(urls, globals())

    app.run()
