from collections import OrderedDict
import struct
import sys
import time

from ..core import SMBusDriver, run_drivers
from smbus2 import SMBus


class Driver(SMBusDriver):
    _CMD_MOVE = 0x4D
    _CMD_READ = 0x52


    def __init__(self, address, bus=1, movement=None, drivers=None,
        interval=0, polling_interval=0.1, check_move=True):
        super().__init__(bus)
        self._address = address
        self._busnum = bus
        self._movement = movement
        self._drivers = drivers
        self._interval = interval
        self._polling_interval = polling_interval
        self._check_move = check_move


    def run(self):
        self._move(0, 0, 0)
        for vert in _get_range(self._movement["vert"]):
            for pan in _get_range(self._movement["pan"]):
                for tilt in _get_range(self._movement["tilt"]):
                    self._move(vert, pan, tilt)
                    vert, pan, tilt, flags, bt1, bt2 = self._read_state()
                    state = OrderedDict([
                        ("vert"    , vert),
                        ("pan"     , pan),
                        ("tilt"    , tilt),
                        ("flags"   , flags),
                        ("battery1", bt1),
                        ("battery2", bt2),
                    ])
                    yield self.sid(), int(time.time() * 1e9), state
                    if self._drivers:
                        self._bus.close()
                        if self._lock: self._lock.release()
                        yield from run_drivers(self._drivers, self._interval)
                        if self._lock: self._lock.acquire()
                        self._bus = SMBus(self._busnum)


    def _move(self, vert, pan, tilt):
        data = struct.pack(">HBB", vert, pan, tilt)
        _retry(lambda: self._bus.write_i2c_block_data(
            self._address, self._CMD_MOVE, data), 0.5)
        if self._check_move:
            while True:
                time.sleep(self._polling_interval)
                cvert, cpan, ctilt, _, _, _ = self._read_state()
                if cvert == vert and cpan == pan and ctilt == tilt:
                    break
        else:
            time.sleep(self._polling_interval)
        time.sleep(0.1)


    def _read_state(self):
        data = _retry(lambda: self._bus.read_i2c_block_data(
            self._address, self._CMD_READ_STATE, 7), 0.5)
        return struct.unpack(">HBBBBB", data)


def _retry(func, interval):
    while True:
        try:
            return func()
        except OSError:
            print("[vertpantilt] OSError", file=sys.stderr)
            time.sleep(interval)


def _get_range(cfg):
    return range(cfg["start"], cfg["stop"] + 1, cfg["step"])


def _close(a, b, tolerance):
    return abs(a - b) <= tolerance
