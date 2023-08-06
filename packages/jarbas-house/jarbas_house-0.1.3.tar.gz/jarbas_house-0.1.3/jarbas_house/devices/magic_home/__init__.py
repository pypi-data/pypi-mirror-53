from jarbas_house.devices import GenericDevice, RGBWBulb, RGBBulb, Bulb
from jarbas_house.devices.magic_home.magichome import BulbScanner, WifiLedBulb, PresetPattern
from jarbas_house.colors import Color


class MagicHomeDevice(GenericDevice):
    def __init__(self, host, name="generic magic_home device", raw_data=None, product_model="magic_home"):
        raw_data = raw_data or {"name": name, "description": "uses magic home app"}
        super().__init__(host, name, raw_data)
        self._product_model = product_model or name

    @property
    def as_dict(self):
        return {
            "host": self.host,
            "name": self.name,
            "model": self.product_model,
            "device_type": "generic magic_home device",
            "device_id": self.device_id,
            "state": self.is_on,
            "online": self.is_online,
            "raw": self.raw_data
        }

    @property
    def product_model(self):
        return self._product_model

    @property
    def is_online(self):
        return self.raw_data.get("online", True)

    @property
    def device_id(self):
        return self.raw_data.get("id")


class MagicHomeBulb(MagicHomeDevice, Bulb):

    def __init__(self, host, name="light bulb", raw_data=None, product_model="magic_home"):
        super().__init__(host, name, raw_data, product_model=product_model)
        self._bulb = WifiLedBulb(self.host)
        self._timer = None

    @property
    def as_dict(self):
        return {
            "host": self.host,
            "name": self.name,
            "model": self.product_model,
            "device_type": "magic_home light bulb",
            "device_id": self.device_id,
            "brightness": self.brightness_255,
            "state": self.is_on,
            "online": self.is_online,
            "raw": self.raw_data
        }

    @property
    def is_on(self):
        return self._bulb.is_on

    # status change
    def turn_on(self):
        self._bulb.turn_on()

    def turn_off(self):
        self._bulb.turn_off()


class MagicHomeRGBBulb(MagicHomeBulb, RGBBulb):

    def __init__(self, host, name="rgb light bulb", raw_data=None, product_model="magic_home"):
        super().__init__(host, name, raw_data, product_model=product_model)
        self._bulb = WifiLedBulb(self.host)

    def set_preset_pattern(self, pattern, speed=80):
        self._bulb.set_preset_pattern(pattern, speed)

    @property
    def as_dict(self):
        return {
            "host": self.host,
            "name": self.name,
            "model": self.product_model,
            "device_type": "magic_home rgb light bulb",
            "color": self.color.as_dict,
            "brightness": self.brightness_255,
            "device_id": self.device_id,
            "state": self.is_on,
            "online": self.is_online,
            "raw": self.raw_data
        }

    @property
    def color(self):
        if self.is_off:
            return Color.from_name("black")
        return Color(*self._bulb.rgb)

    def change_brightness(self, value, percent=True):
        self._bulb.set_rgb(*self.color.rgb, brightness=value)

    def change_color(self, color):
        if isinstance(color, Color):
            color = color.rgb
            if color == (0, 0, 0):
                self.turn_off()
            else:
                if self.is_off:
                    self.turn_on()
                self._bulb.set_rgb(*color)
        else:
            color = Color.from_name(color)
            self.change_color(color)

    @property
    def preset_patterns(self):
        return {
            "seven_color_cross_fade": PresetPattern.seven_color_cross_fade,
            "red_gradual_change": PresetPattern.red_gradual_change,
            "green_gradual_change": PresetPattern.green_gradual_change,
            "blue_gradual_change": PresetPattern.blue_gradual_change,
            "yellow_gradual_change": PresetPattern.yellow_gradual_change,
            "cyan_gradual_change": PresetPattern.cyan_gradual_change,
            "purple_gradual_change": PresetPattern.purple_gradual_change,
            "white_gradual_change": PresetPattern.white_gradual_change,
            "red_green_cross_fade": PresetPattern.red_green_cross_fade,
            "red_blue_cross_fade": PresetPattern.red_blue_cross_fade,
            "green_blue_cross_fade": PresetPattern.green_blue_cross_fade,
            "seven_color_strobe_flash": PresetPattern.seven_color_strobe_flash,
            "red_strobe_flash": PresetPattern.red_strobe_flash,
            "green_strobe_flash": PresetPattern.green_strobe_flash,
            "blue_strobe_flash": PresetPattern.blue_strobe_flash,
            "yellow_strobe_flash": PresetPattern.yellow_strobe_flash,
            "cyan_strobe_flash": PresetPattern.cyan_strobe_flash,
            "purple_strobe_flash": PresetPattern.purple_strobe_flash,
            "white_strobe_flash": PresetPattern.white_strobe_flash,
            "seven_color_jumping": PresetPattern.seven_color_jumping
        }

    def seven_color_cross_fade(self):
        self.set_preset_pattern(self.preset_patterns["seven_color_cross_fade"])

    def red_gradual_change(self):
        self.set_preset_pattern(self.preset_patterns["red_gradual_change"])

    def green_gradual_change(self):
        self.set_preset_pattern(self.preset_patterns["green_gradual_change"])

    def blue_gradual_change(self):
        self.set_preset_pattern(self.preset_patterns["blue_gradual_change"])

    def yellow_gradual_change(self):
        self.set_preset_pattern(self.preset_patterns["yellow_gradual_change"])

    def cyan_gradual_change(self):
        self.set_preset_pattern(self.preset_patterns["cyan_gradual_change"])

    def purple_gradual_change(self):
        self.set_preset_pattern(self.preset_patterns["purple_gradual_change"])

    def white_gradual_change(self):
        self.set_preset_pattern(self.preset_patterns["white_gradual_change"])

    def red_green_cross_fade(self):
        self.set_preset_pattern(self.preset_patterns["red_green_cross_fade"])

    def red_blue_cross_fade(self):
        self.set_preset_pattern(self.preset_patterns["red_blue_cross_fade"])

    def green_blue_cross_fade(self):
        self.set_preset_pattern(self.preset_patterns["green_blue_cross_fade"])

    def seven_color_strobe_flash(self):
        self.set_preset_pattern(self.preset_patterns["seven_color_strobe_flash"])

    def red_strobe_flash(self):
        self.set_preset_pattern(self.preset_patterns["red_strobe_flash"])

    def green_strobe_flash(self):
        self.set_preset_pattern(self.preset_patterns["green_strobe_flash"])

    def blue_strobe_flash(self):
        self.set_preset_pattern(self.preset_patterns["blue_strobe_flash"])

    def yellow_strobe_flash(self):
        self.set_preset_pattern(self.preset_patterns["yellow_strobe_flash"])

    def cyan_strobe_flash(self):
        self.set_preset_pattern(self.preset_patterns["cyan_strobe_flash"])

    def purple_strobe_flash(self):
        self.set_preset_pattern(self.preset_patterns["purple_strobe_flash"])

    def white_strobe_flash(self):
        self.set_preset_pattern(self.preset_patterns["white_strobe_flash"])

    def seven_color_jumping(self):
        self.set_preset_pattern(self.preset_patterns["seven_color_jumping"])


class MagicHomeRGBWBulb(MagicHomeRGBBulb, RGBWBulb):

    def __init__(self, host, name="rgbw light bulb", raw_data=None, product_model="magic_home"):
        super().__init__(host, name, raw_data, product_model=product_model)

    def reset(self):
        self.mode = ""
        self._timer = None
        if self.is_off:
            self.turn_on()
            from time import sleep
            sleep(0.5)
        self.set_warm_white_255(255)

    @property
    def as_dict(self):
        return {
            "host": self.host,
            "name": self.name,
            "model": self.product_model,
            "device_type": "magic_home rgbw light bulb",
            "color": self.color.as_dict,
            "brightness": self.brightness_255,
            "device_id": self.device_id,
            "state": self.is_on,
            "online": self.is_online,
            "raw": self.raw_data
        }

    def set_warm_white(self, level, persist=True, retry=2):
        self._bulb.set_warm_white(level, persist, retry)

    def set_warm_white_255(self, level, persist=True, retry=2):
        self._bulb.set_warm_white_255(level, persist, retry)

    def set_cold_white(self, level, persist=True, retry=2):
        self._bulb.set_cold_white(level, persist, retry)

    def set_cold_white_255(self, level, persist=True, retry=2):
        self._bulb.set_cold_white_255(level, persist, retry)

    def set_white_temperature(self, temperature, brightness,
                              persist=True, retry=2):
        # Assume output temperature of between 2700 and 6500 Kelvin, and scale
        # the warm and cold LEDs linearly to provide that
        self._bulb.set_white_temperature(temperature, brightness, persist, retry)

    @property
    def warm_white(self):
        return self._bulb.warm_white

    @property
    def warm_white_255(self):
        return self._bulb.warm_white_255

    @property
    def cold_white(self):
        return self._bulb.cold_white


# Product models
# add more to this list when support is added
# refers to "model" key
MAGICHOME_BRAND_LOOKUP = {
    "AK001-ZJ210": MagicHomeRGBWBulb
}


def scan_magichome():
    scanner = BulbScanner()
    scanner.scan(timeout=2)
    devices = scanner.get_bulb_info()
    for d in devices:
        product_model = d.get("model", "magic_home")
        host = d.get("ipaddr")
        clazz = MAGICHOME_BRAND_LOOKUP.get(product_model) or MagicHomeDevice
        d["name"] = d.get("name") or clazz.__name__
        yield clazz(host, d["name"], d, product_model=product_model)


def get_device(ip):
    for device in scan_magichome():
        if device.host == ip:
            return device
    return None


if __name__ == '__main__':
    from pprint import pprint
    from time import sleep


    bulb = get_device('192.168.1.65')
    bulb.change_color("cyan")
    print(bulb.__dict__)

    bulb.set_warm_white_255(255)
    # bulb.color_cycle()
    # sleep(60)
    # bulb.reset()
