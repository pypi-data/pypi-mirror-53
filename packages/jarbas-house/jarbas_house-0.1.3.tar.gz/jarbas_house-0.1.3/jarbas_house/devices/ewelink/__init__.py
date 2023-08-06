from jarbas_house.devices import GenericDevice, Bulb
from jarbas_house.settings import EWELINK_API_REGION, EWELINK_PASSWORD, EWELINK_USERNAME, EWELINK_API_KEY, \
    EWELINK_API_TOKEN
from jarbas_house.devices.ewelink.sonoff import Sonoff
from jarbas_house.colors import Color
from threading import Thread
from time import sleep


class EwelinkDevice(GenericDevice):
    _sonoff = Sonoff(EWELINK_USERNAME, EWELINK_PASSWORD, EWELINK_API_REGION, EWELINK_API_KEY, EWELINK_API_TOKEN)

    def __init__(self, host, name="generic ewelink device", raw_data=None, product_model="ewelink"):
        raw_data = raw_data or {"name": name, "description": "uses ewelink app"}
        super().__init__(host, name, raw_data)
        self._product_model = product_model or name

    @property
    def as_dict(self):
        return {
            "host": self.host,
            "name": self.name,
            "device_type": "generic ewelink device",
            "device_id": self.device_id,
            "state": self.is_on,
            "online": self.is_online,
            "raw": self.raw_data
        }

    @property
    def is_online(self):
        return self.raw_data.get("online")

    @property
    def product_model(self):
        return self._product_model

    @property
    def is_on(self):
        return self.raw_data.get("params", {}).get("state", "off") == "on"

    @property
    def device_id(self):
        return self.raw_data.get("deviceid")

    # status change
    def turn_on(self):
        self._sonoff.update_params(self.raw_data, {'state': "on"})
        bucket = self.raw_data
        bucket["params"]["state"] = "on"
        self._raw.append(bucket)

    def turn_off(self):
        self._sonoff.update_params(self.raw_data, {'state': "off"})
        bucket = self.raw_data
        bucket["params"]["state"] = "off"
        self._raw.append(bucket)


class EwelinkBulb(EwelinkDevice, Bulb):
    def __init__(self, host, name="bulb", raw_data=None, product_model="ewelink"):
        super().__init__(host, name, raw_data, product_model=product_model)


class MosquitoKiller(EwelinkBulb):
    def __init__(self, host, name="mosquito killer", raw_data=None, product_model="ewelink"):
        super().__init__(host, name, raw_data, product_model=product_model)
        self.mode = ""
        self._timer = None

    @property
    def color(self):
        if self.is_off:
            return Color.from_name("black")
        return Color.from_name("violet")

    def change_color(self, color="violet"):
        if isinstance(color, Color):
            if color.rgb == (0, 0, 0):
                self.turn_off()
            else:
                if self.is_off:
                    self.turn_on()
                if Color.from_name("violet") != color:
                    print("ERROR: mosquito killer does not support color change")
        else:
            color = Color.from_name(color)
            self.change_color(color)

    @property
    def as_dict(self):
        return {
            "host": self.host,
            "name": self.name,
            "model": self.product_model,
            "device_type": "mosquito killer",
            "brightness": self.brightness_255,
            "device_id": self.device_id,
            "state": self.is_on,
            "online": self.is_online,
            "raw": self.raw_data
        }

    @property
    def brightness_255(self):
        """
        Return current brightness 0-255
        """
        return self.raw_data["params"]['channel0']

    def change_brightness(self, value, percent=True):
        self.change_channel(0, value, percent)

    def change_channel(self, n, value, percent=True):
        # 0 - brightness
        # 1 - 4 - seem to do nothing ?
        assert 0 <= n <= 4
        if isinstance(value, str):
            value = int(value)

        if percent and isinstance(value, int):
            value = value * 255 / 100
        elif percent and isinstance(value, float) and 0 <= value <= 1:  # 0.1
            value = value * 255

        value = str(int(value))
        # print("Changing mosquito killer light channel: {n} to value: {value}".format(n=n,
        #                                                                             value=value))
        self._sonoff.update_params(self.raw_data, {'channel' + str(n): value})
        bucket = self.raw_data
        bucket["params"]['channel' + str(n)] = value
        self._raw.append(bucket)

    def blink(self, speed=0):

        self.mode = "blink"
        if self.is_off:
            self.turn_on()

        def cycle():
            while self.mode == "blink":
                self.change_brightness(10)
                sleep(0.5)
                self.change_brightness(100)
                sleep(0.5)

        self._timer = Thread(target=cycle)
        self._timer.setDaemon(True)
        self._timer.start()

    def reset(self):
        self.mode = ""
        self.turn_on()
        self.set_high_brightness()
        self._timer = None


# Product models
# add more to this list when support is added
# refers to productModel field
EWELINK_BRAND_LOOKUP = {
    'LA-1CUI': MosquitoKiller
}


def scan_ewelink():
    s = Sonoff(EWELINK_USERNAME, EWELINK_PASSWORD, EWELINK_API_REGION)
    devices = s.get_devices()
    if devices:
        for d in devices:
            product_model = d.get("productModel", "ewelink")
            name = d.get("name", "generic_device")
            host = d.get("ip")
            clazz = EWELINK_BRAND_LOOKUP.get(product_model) or EwelinkDevice
            yield clazz(host, name, d, product_model=product_model)


def get_device(ip):
    for device in scan_ewelink():
        if device.host == ip:
            return device
    return None


if __name__ == "__main__":
    from pprint import pprint
    from time import sleep

    mosquito = get_device("89.181.81.195")
    if mosquito:
        mosquito.toggle()
        print(mosquito.__class__.__name__)

    exit()
    for d in scan_ewelink():
        pprint(d.as_dict)
        # print(d.name, d.host, d.is_on, d.is_online)
