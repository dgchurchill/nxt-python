
from nxt.brick import Brick
from glob import glob

class DeviceSocket:
    def __init__(self, filename=None):
        if filename is None:
            matches = glob('/dev/*-DevB')
            if len(matches) == 0:
                raise IOError("No device found")
            filename = matches[0]

        self._filename = filename

    def connect(self):
        self._device = open(self._filename, 'r+b', buffering=0)
        return Brick(self)
    
    def close(self):
        self._device.close()
    
    def send(self, data):
        l0 = len(data) & 0xFF
        l1 = (len(data) >> 8) & 0xFF
        d = chr(l0) + chr(l1) + data
        self._device.write(d)

    def recv(self):
        data = self._device.read(2)
        l0 = ord(data[0])
        l1 = ord(data[1])
        plen = l0 + (l1 << 8)
        return self._device.read(plen)
