import json
import re
import threading
from time import sleep

import requests
from pyinnotemp.rooms import BBRooms


class BBConnector:

    def __init__(self):
        raw_params = {'un': 'admin', 'pw': '123456'}
        self.session = requests.Session()
        self.roomList = []
        r = self.session.post("http://biccbox/inc/groups.read.php", data=raw_params)
        r = self.session.post("http://biccbox/inc/roomconf.read.php")
        self._roomsraw = json.loads(r.text)
        for rooms in self._roomsraw['room']:
            attr = rooms['@attributes']
            if attr['label'] != 'Heizraum':
                roomno = int(re.search(r'\d+', attr['type']).group())
                raw_params_getroom = {'un': 'admin', 'pw': '123456', 'room_id': str(roomno)}
                r = requests.post("http://biccbox/inc/value.read.php", raw_params_getroom)
                jn = json.loads(r.text)
                setvar = list(jn.keys())[0]
                targetvar = rooms['main']['input'][0]['var']
                sensorvar = rooms['main']['input'][1]['var']
                statusvar = rooms['main']['input'][3]['var']
                self.roomList.append(BBRooms(attr['label'], roomno, targetvar, sensorvar, statusvar, setvar))
        self.lastUpdate = 0.0

    def _startUpdateThread(self):
        # Only call this function once
        self.update_thread = threading.Thread(target=self._updateLoop)
        self.update_thread.daemon = True
        self.update_thread.start()

    def _stopUpdateThread(self):
        # Only call this function once
        self.update_thread.daemon = False
        self.update_thread.join()


    def _updateLoop(self):
        print("Starting Update Thread")
        while True:
            self.update()
            sleep(15)

    def update(self):
        print('Starting Update')
        r = self.session.post("http://biccbox/inc/live_signal.read.php")
        jnresponse = json.loads(r.text)
        print(jnresponse)
        for room in self.roomList:
            room.updateCurrentTemperature(jnresponse[room.getSensorVariable()])
            room.updateTargetTemperature(jnresponse[room.getTargetVariable()])
        self.lastUpdate = jnresponse['sysTime']

    def start(self):
        print('Starting Innotemp Service')
        self._startUpdateThread()

    def stop(self):
        self._stopUpdateThread()