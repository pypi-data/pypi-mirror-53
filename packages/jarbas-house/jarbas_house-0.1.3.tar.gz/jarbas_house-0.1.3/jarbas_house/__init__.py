from jarbas_house.devices import GenericDevice
from jarbas_house.util import merge_dict
import time
from threading import Timer


class House:
    def __init__(self, name="house", scanners=None, verbose=True, device_timeout=2):
        self._name = name
        self.scanners = scanners or []
        self._devices = {}
        self._timestamps = {}
        self._device_timeout = device_timeout * 60
        self._monitor_pause = 10
        self.verbose = verbose
        self._timer = None
        self.monitoring = False
        self._on_new_device_handlers = []
        self._on_device_seen_handlers = []
        self._on_device_updated_handlers = []
        self._on_device_lost_handlers = []

    def add_scanner(self, func):
        self.scanners.append(func)

    def add_device(self, device):
        assert isinstance(device, GenericDevice)
        self.devices[device.host] = device

    def remove_device(self, device):
        if isinstance(device, GenericDevice):
            host = device.host
        else:
            host = str(device)
        self.devices.pop(host)
        self._timestamps.pop(host)

    def update_device(self, device):
        assert isinstance(device, GenericDevice)
        # TODO make this part of device class
        if device.raw_data not in self._devices[device.host]._raw:
            self._devices[device.host]._raw.append(device.raw_data)
            if self.verbose:
                print("DEBUG: updating device data {device}".format(device=self._devices[device.host]))
            for handler in self._on_device_updated_handlers:
                try:
                    handler(device)
                except Exception as e:
                    if self.verbose:
                        print("ERROR: exception in on_device_updated handler - {e}".format(e=e))

            if device.name:
                self._devices[device.host]._name = device.name
            # TODO implement an hierarchy for class morphing
            if self._devices[device.host].__class__ == GenericDevice and device.__class__ != GenericDevice:
                if self.verbose:
                    print("DEBUG: updating device class {device}".format(device=self._devices[device.host]))
                self._devices[device.host].__class__ = device.__class__

    @property
    def devices(self):
        return self._devices

    @property
    def name(self):
        return self._name

    def scan_devices(self):
        for scanner in self.scanners:
            for device in scanner():
                yield device

    def start(self):
        self.monitoring = True
        self._timer = Timer(self._monitor_pause, self._monitor)
        self._timer.setDaemon(True)
        self._timer.start()

    def stop(self):
        self.monitoring = False
        self._timer = None

    def _monitor(self):
        if self.monitoring:
            for device in self.scan_devices():
                if device.host not in self._devices:
                    if self.verbose:
                        print("INFO: new device:{device}".format(device=device))
                    for handler in self._on_new_device_handlers:
                        try:
                            handler(device)
                        except Exception as e:
                            if self.verbose:
                                print("ERROR: exception in on_new_device handler - {e}".format(e=e))
                    self.add_device(device)
                else:
                    for handler in self._on_device_seen_handlers:
                        try:
                            handler(device)
                        except Exception as e:
                            if self.verbose:
                                print("ERROR: exception in on_device_seen handler - {e}".format(e=e))
                    self.update_device(device)

                if device.host not in self._timestamps:
                    self._timestamps[device.host] = []
                self._timestamps[device.host] += [time.time()]

            now = time.time()
            for device in dict(self._timestamps):
                last_seen = now - self._timestamps[device][-1]
                if self.verbose:
                    print(
                        "DEBUG: device {device}, last seen {seconds} seconds ago ".format(device=self._devices[device],
                                                                                          seconds=last_seen))
                if last_seen >= self._device_timeout or not self._devices[device].is_online:
                    if self.verbose:
                        print("INFO: lost device: {device}".format(device=self._devices[device]))
                    for handler in self._on_device_lost_handlers:
                        try:
                            handler(device)
                        except Exception as e:
                            if self.verbose:
                                print("ERROR: exception in on_device_lost handler - {e}".format(e=e))
                    self.remove_device(device)

            self.start()

    def on_new_device(self, handler):
        self._on_new_device_handlers.append(handler)

    def on_device_lost(self, handler):
        self._on_device_lost_handlers.append(handler)

    def on_device_seen(self, handler):
        self._on_device_seen_handlers.append(handler)

    def on_device_updated(self, handler):
        self._on_device_updated_handlers.append(handler)

    def remove_handlers(self):
        self._on_new_device_handlers = []
        self._on_device_seen_handlers = []
        self._on_device_lost_handlers = []
        self._on_device_updated_handlers = []


if __name__ == "__main__":
    from pprint import pprint
    from jarbas_house.devices.ewelink import scan_ewelink
    from jarbas_house.devices.tplink import scan_kasa
    from jarbas_house.devices.magic_home import scan_magichome
    from jarbas_house.devices.scan import scan_bluetooth, scan_wifi

    house = House()
    house.add_scanner(scan_wifi)
    house.add_scanner(scan_bluetooth)
    house.add_scanner(scan_magichome)
    house.add_scanner(scan_kasa)
    house.add_scanner(scan_ewelink)

    # for d in house.scan_devices():
    #    pprint(d.as_dict)

    # house = House()

    house.start()
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        house.stop()
