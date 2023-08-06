#!/usr/bin/env python

"""
This is a utility for controlling stand-alone Flux WiFi LED light bulbs.
The protocol was reverse-engineered by studying packet captures between a
bulb and the controlling "Magic Home" mobile app.  The code here dealing
with the network protocol is littered with magic numbers, and ain't so pretty.
But it does seem to work!

So far most of the functionality of the apps is available here via the CLI
and/or programmatically.

The classes in this project could very easily be used as an API, and incorporated into a GUI app written
in PyQt, Kivy, or some other framework.

##### Available:
* Discovering bulbs on LAN
* Turning on/off bulb
* Get state information
* Setting "warm white" mode
* Setting single color mode
* Setting preset pattern mode
* Setting custom pattern mode
* Reading timers
* Setting timers

##### Some missing pieces:
* Initial administration to set up WiFi SSID and passphrase/key.
* Remote access administration
* Music-relating pulsing. This feature isn't so impressive on the Magic Home app,
and looks like it might be a bit of work.
"""

import socket
import time
import datetime
import colorsys
import threading
from jarbas_house.devices.magic_home import utils


class PresetPattern(object):
    seven_color_cross_fade = 0x25
    red_gradual_change = 0x26
    green_gradual_change = 0x27
    blue_gradual_change = 0x28
    yellow_gradual_change = 0x29
    cyan_gradual_change = 0x2a
    purple_gradual_change = 0x2b
    white_gradual_change = 0x2c
    red_green_cross_fade = 0x2d
    red_blue_cross_fade = 0x2e
    green_blue_cross_fade = 0x2f
    seven_color_strobe_flash = 0x30
    red_strobe_flash = 0x31
    green_strobe_flash = 0x32
    blue_strobe_flash = 0x33
    yellow_strobe_flash = 0x34
    cyan_strobe_flash = 0x35
    purple_strobe_flash = 0x36
    white_strobe_flash = 0x37
    seven_color_jumping = 0x38

    @staticmethod
    def valid(pattern):
        if pattern < 0x25 or pattern > 0x38:
            return False
        return True

    @staticmethod
    def valtostr(pattern):
        for key, value in list(PresetPattern.__dict__.items()):
            if type(value) is int and value == pattern:
                return key.replace("_", " ").title()
        return None


class BuiltInTimer(object):
    sunrise = 0xA1
    sunset = 0xA2

    @staticmethod
    def valid(byte_value):
        return byte_value == BuiltInTimer.sunrise or byte_value == BuiltInTimer.sunset

    @staticmethod
    def valtostr(pattern):
        for key, value in list(BuiltInTimer.__dict__.items()):
            if type(value) is int and value == pattern:
                return key.replace("_", " ").title()
        return None


class LedTimer(object):
    Mo = 0x02
    Tu = 0x04
    We = 0x08
    Th = 0x10
    Fr = 0x20
    Sa = 0x40
    Su = 0x80
    Everyday = Mo | Tu | We | Th | Fr | Sa | Su
    Weekdays = Mo | Tu | We | Th | Fr
    Weekend = Sa | Su

    @staticmethod
    def dayMaskToStr(mask):
        for key, value in list(LedTimer.__dict__.items()):
            if type(value) is int and value == mask:
                return key
        return None

    def __init__(self, bytes=None):
        if bytes is not None:
            self.fromBytes(bytes)
            return

        the_time = datetime.datetime.now() + datetime.timedelta(hours=1)
        self.setTime(the_time.hour, the_time.minute)
        self.setDate(the_time.year, the_time.month, the_time.day)
        self.setModeTurnOff()
        self.setActive(False)

    def setActive(self, active=True):
        self.active = active

    def isActive(self):
        return self.active

    def isExpired(self):
        # if no repeat mask and datetime is in past, return True
        if self.repeat_mask != 0:
            return False
        elif self.year != 0 and self.month != 0 and self.day != 0:
            dt = datetime.datetime(self.year, self.month, self.day, self.hour, self.minute)
            if utils.date_has_passed(dt):
                return True
        return False

    def setTime(self, hour, minute):
        self.hour = hour
        self.minute = minute

    def setDate(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
        self.repeat_mask = 0

    def setRepeatMask(self, repeat_mask):
        self.year = 0
        self.month = 0
        self.day = 0
        self.repeat_mask = repeat_mask

    def setModeDefault(self):
        self.mode = "default"
        self.pattern_code = 0
        self.turn_on = True
        self.red = 0
        self.green = 0
        self.blue = 0
        self.warmth_level = 0

    def setModePresetPattern(self, pattern, speed):
        self.mode = "preset"
        self.warmth_level = 0
        self.pattern_code = pattern
        self.delay = utils.speed_to_delay(speed)
        self.turn_on = True

    def setModeColor(self, r, g, b):
        self.mode = "color"
        self.warmth_level = 0
        self.red = r
        self.green = g
        self.blue = b
        self.pattern_code = 0x61
        self.turn_on = True

    def setModeWarmWhite(self, level):
        self.mode = "ww"
        self.warmth_level = utils.percent_to_byte(level)
        self.pattern_code = 0x61
        self.red = 0
        self.green = 0
        self.blue = 0
        self.turn_on = True

    def setModeSunrise(self, startBrightness, endBrightness, duration):
        self.mode = "sunrise"
        self.turn_on = True
        self.pattern_code = BuiltInTimer.sunrise
        self.brightness_start = utils.percent_to_byte(startBrightness)
        self.brightness_end = utils.percent_to_byte(endBrightness)
        self.warmth_level = utils.percent_to_byte(endBrightness)
        self.duration = int(duration)

    def setModeSunset(self, startBrightness, endBrightness, duration):
        self.mode = "sunrise"
        self.turn_on = True
        self.pattern_code = BuiltInTimer.sunset
        self.brightness_start = utils.percent_to_byte(startBrightness)
        self.brightness_end = utils.percent_to_byte(endBrightness)
        self.warmth_level = utils.percent_to_byte(endBrightness)
        self.duration = int(duration)

    def setModeTurnOff(self):
        self.mode = "off"
        self.turn_on = False
        self.pattern_code = 0

    """

    timer are in six 14-byte structs
        f0 0f 08 10 10 15 00 00 25 1f 00 00 00 f0 0f
         0  1  2  3  4  5  6  7  8  9 10 11 12 13 14

        0: f0 when active entry/ 0f when not active
        1: (0f=15) year when no repeat, else 0
        2:  month when no repeat, else 0
        3:  dayofmonth when no repeat, else 0
        4: hour
        5: min
        6: 0
        7: repeat mask, Mo=0x2,Tu=0x04, We 0x8, Th=0x10 Fr=0x20, Sa=0x40, Su=0x80
        8:  61 for solid color or warm, or preset pattern code
        9:  r (or delay for preset pattern)
        10: g
        11: b
        12: warm white level
        13: 0f = off, f0 = on ?
    """

    def fromBytes(self, bytes):
        # utils.dump_bytes(bytes)
        self.red = 0
        self.green = 0
        self.blue = 0
        if bytes[0] == 0xf0:
            self.active = True
        else:
            self.active = False
        self.year = bytes[1] + 2000
        self.month = bytes[2]
        self.day = bytes[3]
        self.hour = bytes[4]
        self.minute = bytes[5]
        self.repeat_mask = bytes[7]
        self.pattern_code = bytes[8]

        if self.pattern_code == 0x00:
            self.mode = "default"
        elif self.pattern_code == 0x61:
            self.mode = "color"
            self.red = bytes[9]
            self.green = bytes[10]
            self.blue = bytes[11]
        elif BuiltInTimer.valid(self.pattern_code):
            self.mode = BuiltInTimer.valtostr(self.pattern_code)
            self.duration = bytes[9]  # same byte as red
            self.brightness_start = bytes[10]  # same byte as green
            self.brightness_end = bytes[11]  # same byte as blue
        elif PresetPattern.valid(self.pattern_code):
            self.mode = "preset"
            self.delay = bytes[9]  # same byte as red
        else:
            self.mode = "unknown"

        self.warmth_level = bytes[12]
        if self.warmth_level != 0:
            self.mode = "ww"

        if bytes[13] == 0xf0:
            self.turn_on = True
        else:
            self.turn_on = False
            self.mode = "off"

    def toBytes(self):
        bytes = bytearray(14)
        if not self.active:
            bytes[0] = 0x0f
            # quit since all other zeros is good
            return bytes

        bytes[0] = 0xf0

        if self.year >= 2000:
            bytes[1] = self.year - 2000
        else:
            bytes[1] = self.year
        bytes[2] = self.month
        bytes[3] = self.day
        bytes[4] = self.hour
        bytes[5] = self.minute
        # what is 6?
        bytes[7] = self.repeat_mask

        if not self.turn_on:
            bytes[13] = 0x0f
            return bytes
        bytes[13] = 0xf0

        bytes[8] = self.pattern_code
        if PresetPattern.valid(self.pattern_code):
            bytes[9] = self.delay
            bytes[10] = 0
            bytes[11] = 0
        elif BuiltInTimer.valid(self.pattern_code):
            bytes[9] = self.duration
            bytes[10] = self.brightness_start
            bytes[11] = self.brightness_end
        else:
            bytes[9] = self.red
            bytes[10] = self.green
            bytes[11] = self.blue
        bytes[12] = self.warmth_level

        return bytes

    def __str__(self):
        txt = ""
        if not self.active:
            return "Unset"

        if self.turn_on:
            txt += "[ON ]"
        else:
            txt += "[OFF]"

        txt += " "

        txt += "{:02}:{:02}  ".format(self.hour, self.minute)

        if self.repeat_mask == 0:
            txt += "Once: {:04}-{:02}-{:02}".format(self.year, self.month, self.day)
        else:
            bits = [LedTimer.Su, LedTimer.Mo, LedTimer.Tu, LedTimer.We, LedTimer.Th, LedTimer.Fr, LedTimer.Sa]
            for b in bits:
                if self.repeat_mask & b:
                    txt += LedTimer.dayMaskToStr(b)
                else:
                    txt += "--"
            txt += "  "

        txt += "  "
        if self.pattern_code == 0x61:
            if self.warmth_level != 0:
                txt += "Warm White: {}%".format(utils.byte_to_percent(self.warmth_level))
            else:
                color_str = utils.color_tuple_to_string((self.red, self.green, self.blue))
                txt += "Color: {}".format(color_str)

        elif PresetPattern.valid(self.pattern_code):
            pat = PresetPattern.valtostr(self.pattern_code)
            speed = utils.delay_to_speed(self.delay)
            txt += "{} (Speed:{}%)".format(pat, speed)

        elif BuiltInTimer.valid(self.pattern_code):
            type = BuiltInTimer.valtostr(self.pattern_code)

            txt += "{} (Duration:{} minutes, Brightness: {}% -> {}%)".format(
                type, self.duration,
                utils.byte_to_percent(self.brightness_start), utils.byte_to_percent(self.brightness_end))

        return txt


class WifiLedBulb(object):
    def __init__(self, ipaddr, port=5577, timeout=5):
        self.ipaddr = ipaddr
        self.port = port
        self.timeout = timeout

        self.protocol = None
        self.rgbwcapable = False
        self.rgbwprotocol = False

        self.raw_state = None
        self._is_on = False
        self._mode = None
        self._socket = None
        self._lock = threading.Lock()
        self._query_len = 0
        self._use_csum = True

        self.connect(2)
        self.update_state()

    @property
    def mode(self):
        return self._mode

    @property
    def warm_white(self):
        if self.protocol == 'LEDENET':
            return self.raw_state[9]
        else:
            return 0

    @property
    def cold_white(self):
        if self.protocol == 'LEDENET':
            return self.raw_state[11]
        else:
            return 0

    @property
    def brightness(self):
        """Return current brightness 0-255.

        For warm white return current led level. For RGB
        calculate the HSV and return the 'value'.
        """
        if self.mode == "ww":
            return int(self.raw_state[9])
        else:
            _, _, v = colorsys.rgb_to_hsv(*self.rgb)
            return v

    def connect(self, retry=0):
        self.close()
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.settimeout(self.timeout)
            self._socket.connect((self.ipaddr, self.port))
        except socket.error:
            if retry < 1:
                return
            self.connect(max(retry - 1, 0))

    def close(self):
        if self._socket is None:
            return
        try:
            self._socket.close()
        except socket.error:
            pass

    def _determine_mode(self, ww_level, pattern_code):
        mode = "unknown"
        if pattern_code in [0x61, 0x62]:
            if self.rgbwcapable:
                mode = "color"
            elif ww_level != 0:
                mode = "ww"
            else:
                mode = "color"
        elif pattern_code == 0x60:
            mode = "custom"
        elif pattern_code == 0x41:
            mode = "color"
        elif PresetPattern.valid(pattern_code):
            mode = "preset"
        elif BuiltInTimer.valid(pattern_code):
            mode = BuiltInTimer.valtostr(pattern_code)
        return mode

    def _determine_query_len(self, retry=2):

        # determine the type of protocol based of first 2 bytes.
        self._send_msg(bytearray([0x81, 0x8a, 0x8b]))
        rx = self._read_msg(2)
        # if any response is recieved, use the default protocol
        if len(rx) == 2:
            self._query_len = 14
            return
        # if no response from default received, next try the original protocol
        self._send_msg(bytearray([0xef, 0x01, 0x77]))
        rx = self._read_msg(2)
        if rx[1] == 0x01:
            self.protocol = 'LEDENET_ORIGINAL'
            self._use_csum = False
            self._query_len = 11
            return
        else:
            self._use_csum = True
        if rx == None and retry > 0:
            self._determine_query_len(max(retry - 1, 0))

    def query_state(self, retry=2, led_type=None):
        if self._query_len == 0:
            self._determine_query_len()

        # default value
        msg = bytearray([0x81, 0x8a, 0x8b])
        # alternative for original protocol
        if self.protocol == 'LEDENET_ORIGINAL' or led_type == 'LEDENET_ORIGINAL':
            msg = bytearray([0xef, 0x01, 0x77])
            led_type = 'LEDENET_ORIGINAL'

        try:
            self.connect()
            self._send_msg(msg)
            rx = self._read_msg(self._query_len)
        except socket.error:
            if retry < 1:
                self._is_on = False
                return
            self.connect()
            return self.query_state(max(retry - 1, 0), led_type)
        if rx is None or len(rx) < self._query_len:
            if retry < 1:
                self._is_on = False
                return rx
            return self.query_state(max(retry - 1, 0), led_type)
        return rx

    def update_state(self, retry=2):
        rx = self.query_state(retry)
        if rx is None or len(rx) < self._query_len:
            self._is_on = False
            return

        # typical response:
        # pos  0  1  2  3  4  5  6  7  8  9 10
        #    66 01 24 39 21 0a ff 00 00 01 99
        #     |  |  |  |  |  |  |  |  |  |  |
        #     |  |  |  |  |  |  |  |  |  |  checksum
        #     |  |  |  |  |  |  |  |  |  warmwhite
        #     |  |  |  |  |  |  |  |  blue
        #     |  |  |  |  |  |  |  green
        #     |  |  |  |  |  |  red
        #     |  |  |  |  |  speed: 0f = highest f0 is lowest
        #     |  |  |  |  <don't know yet>
        #     |  |  |  preset pattern
        #     |  |  off(23)/on(24)
        #     |  type
        #     msg head
        #

        # response from a 5-channel LEDENET controller:
        # pos  0  1  2  3  4  5  6  7  8  9 10 11 12 13
        #    81 25 23 61 21 06 38 05 06 f9 01 00 0f 9d
        #     |  |  |  |  |  |  |  |  |  |  |  |  |  |
        #     |  |  |  |  |  |  |  |  |  |  |  |  |  checksum
        #     |  |  |  |  |  |  |  |  |  |  |  |  color mode (f0 colors were set, 0f whites, 00 all were set)
        #     |  |  |  |  |  |  |  |  |  |  |  cold-white
        #     |  |  |  |  |  |  |  |  |  |  <don't know yet>
        #     |  |  |  |  |  |  |  |  |  warmwhite
        #     |  |  |  |  |  |  |  |  blue
        #     |  |  |  |  |  |  |  green
        #     |  |  |  |  |  |  red
        #     |  |  |  |  |  speed: 0f = highest f0 is lowest
        #     |  |  |  |  <don't know yet>
        #     |  |  |  preset pattern
        #     |  |  off(23)/on(24)
        #     |  type
        #     msg head
        #

        # Devices that don't require a separate rgb/w bit
        if (rx[1] == 0x04 or
                rx[1] == 0x33 or
                rx[1] == 0x81):
            self.rgbwprotocol = True

        # Devices that actually support rgbw
        if (rx[1] == 0x04 or
                rx[1] == 0x25 or
                rx[1] == 0x33 or
                rx[1] == 0x81):
            self.rgbwcapable = True

        # Devices that use an 8-byte protocol
        if (rx[1] == 0x25 or
                rx[1] == 0x27 or
                rx[1] == 0x35):
            self.protocol = "LEDENET"

        # Devices that use the original LEDENET protocol
        if rx[1] == 0x01:
            self.protocol = "LEDENET_ORIGINAL"
            self._use_csum = False

        pattern = rx[3]
        ww_level = rx[9]
        mode = self._determine_mode(ww_level, pattern)
        if mode == "unknown":
            if retry < 1:
                return
            self.update_state(max(retry - 1, 0))
            return
        power_state = rx[2]

        if power_state == 0x23:
            self._is_on = True
        elif power_state == 0x24:
            self._is_on = False
        self.raw_state = rx
        self._mode = mode

    def __str__(self):
        rx = self.raw_state
        mode = self.mode

        pattern = rx[3]
        ww_level = rx[9]
        power_state = rx[2]
        power_str = "Unknown power state"

        if power_state == 0x23:
            power_str = "ON "
        elif power_state == 0x24:
            power_str = "OFF "

        delay = rx[5]
        speed = utils.delay_to_speed(delay)
        if mode == "color":
            red = rx[6]
            green = rx[7]
            blue = rx[8]
            mode_str = "Color: {}".format((red, green, blue))
            if self.rgbwcapable:
                mode_str += " White: {}".format(rx[9])
            else:
                mode_str += " Brightness: {}".format(self.brightness)
        elif mode == "ww":
            mode_str = "Warm White: {}%".format(utils.byte_to_percent(ww_level))
        elif mode == "preset":
            pat = PresetPattern.valtostr(pattern)
            mode_str = "Pattern: {} (Speed {}%)".format(pat, speed)
        elif mode == "custom":
            mode_str = "Custom pattern (Speed {}%)".format(speed)
        elif BuiltInTimer.valid(pattern):
            mode_str = BuiltInTimer.valtostr(pattern)
        else:
            mode_str = "Unknown mode 0x{:x}".format(pattern)
        if pattern == 0x62:
            mode_str += " (tmp)"
        mode_str += " raw state: "
        for _r in rx:
            mode_str += str(_r) + ","
        return "{} [{}]".format(power_str, mode_str)

    def _change_state(self, retry, turn_on=True):

        if self.protocol == 'LEDENET_ORIGINAL':
            msg_on = bytearray([0xcc, 0x23, 0x33])
            msg_off = bytearray([0xcc, 0x24, 0x33])
        else:
            msg_on = bytearray([0x71, 0x23, 0x0f])
            msg_off = bytearray([0x71, 0x24, 0x0f])

        if turn_on:
            msg = msg_on
        else:
            msg = msg_off

        try:
            self._send_msg(msg)
        except socket.error:
            if retry > 0:
                self.connect()
                self._change_state(max(retry - 1, 0), turn_on)
                return
            self._is_on = False

    def turn_on(self, retry=2):
        self._is_on = True
        self._change_state(retry, turn_on=True)

    def turn_off(self, retry=2):
        self._is_on = False
        self._change_state(retry, turn_on=False)

    @property
    def is_on(self):
        return self._is_on

    @property
    def warm_white_255(self):
        if self.mode != "ww":
            return 255
        return self.brightness

    def set_warm_white(self, level, persist=True, retry=2):
        self.set_warm_white_255(utils.percent_to_byte(level), persist, retry)

    def set_warm_white_255(self, level, persist=True, retry=2):
        self.set_rgbw(w=level, persist=persist, brightness=None, retry=retry)

    def set_cold_white(self, level, persist=True, retry=2):
        self.set_cold_white_255(utils.percent_to_byte(level), persist, retry)

    def set_cold_white_255(self, level, persist=True, retry=2):
        self.set_rgbw(persist=persist, brightness=None, retry=retry, w2=level)

    def set_white_temperature(self, temperature, brightness, persist=True,
                              retry=2):
        # Assume output temperature of between 2700 and 6500 Kelvin, and scale
        # the warm and cold LEDs linearly to provide that
        temperature = max(temperature - 2700, 0)
        warm = 255 * (1 - (temperature // 3800))
        cold = min(255 * temperature // 3800, 255)
        warm *= brightness // 255
        cold *= brightness // 255
        self.set_rgbw(w=warm, w2=cold, persist=persist, retry=retry)

    @property
    def rgbw(self):
        if self.mode != "color":
            return (255, 255, 255, 255)
        red = self.raw_state[6]
        green = self.raw_state[7]
        blue = self.raw_state[8]
        white = self.raw_state[9]
        return (red, green, blue, white)

    @property
    def rgbww(self):
        if self.mode != "color":
            return (255, 255, 255, 255, 255)
        red = self.raw_state[6]
        green = self.raw_state[7]
        blue = self.raw_state[8]
        white = self.raw_state[9]
        white2 = self.raw_state[11]
        return (red, green, blue, white, white2)

    def speed(self):
        delay = self.raw_state[5]
        speed = utils.delay_to_speed(delay)
        return speed

    def set_rgbw(self, r=None, g=None, b=None, w=None, persist=True,
                 brightness=None, retry=2, w2=None):

        if (r or g or b) and (w or w2) and not self.rgbwcapable:
            print("RGBW command sent to non-RGBW device")
            raise Exception

        # sample message for original LEDENET protocol (w/o checksum at end)
        #  0  1  2  3  4
        # 56 90 fa 77 aa
        #  |  |  |  |  |
        #  |  |  |  |  terminator
        #  |  |  |  blue
        #  |  |  green
        #  |  red
        #  head

        # sample message for 8-byte protocols (w/ checksum at end)
        #  0  1  2  3  4  5  6
        # 31 90 fa 77 00 00 0f
        #  |  |  |  |  |  |  |
        #  |  |  |  |  |  |  terminator
        #  |  |  |  |  |  write mask / white2 (see below)
        #  |  |  |  |  white
        #  |  |  |  blue
        #  |  |  green
        #  |  red
        #  persistence (31 for true / 41 for false)
        #
        # byte 5 can have different values depending on the type
        # of device:
        # For devices that support 2 types of white value (warm and cold
        # white) this value is the cold white value. These use the LEDENET
        # protocol. If a second value is not given, reuse the first white value.
        #
        # For devices that cannot set both rbg and white values at the same time
        # (including devices that only support white) this value
        # specifies if this command is to set white value (0f) or the rgb
        # value (f0).
        #
        # For all other rgb and rgbw devices, the value is 00

        # sample message for 9-byte LEDENET protocol (w/ checksum at end)
        #  0  1  2  3  4  5  6  7
        # 31 bc c1 ff 00 00 f0 0f
        #  |  |  |  |  |  |  |  |
        #  |  |  |  |  |  |  |  terminator
        #  |  |  |  |  |  |  write mode (f0 colors, 0f whites, 00 colors & whites)
        #  |  |  |  |  |  cold white
        #  |  |  |  |  warm white
        #  |  |  |  blue
        #  |  |  green
        #  |  red
        #  persistence (31 for true / 41 for false)
        #

        if brightness != None:
            (r, g, b) = self._calculate_brightness((r, g, b), brightness)

        # The original LEDENET protocol
        if self.protocol == 'LEDENET_ORIGINAL':
            msg = bytearray([0x56])
            msg.append(int(r))
            msg.append(int(g))
            msg.append(int(b))
            msg.append(0xaa)
        else:
            # all other devices

            # assemble the message
            if persist:
                msg = bytearray([0x31])
            else:
                msg = bytearray([0x41])

            if r is not None:
                msg.append(int(r))
            else:
                msg.append(int(0))
            if g is not None:
                msg.append(int(g))
            else:
                msg.append(int(0))
            if b is not None:
                msg.append(int(b))
            else:
                msg.append(int(0))
            if w is not None:
                msg.append(int(w))
            else:
                msg.append(int(0))

            if self.protocol == "LEDENET":
                # LEDENET devices support two white outputs for cold and warm. We set
                # the second one here - if we're only setting a single white value,
                # we set the second output to be the same as the first
                if w2 is not None:
                    msg.append(int(w2))
                elif w is not None:
                    msg.append(int(w))
                else:
                    msg.append(0)

            # write mask, default to writing color and whites simultaneously
            write_mask = 0x00
            # rgbwprotocol devices always overwrite both color & whites
            if not self.rgbwprotocol:
                if w is None and w2 is None:
                    # Mask out whites
                    write_mask |= 0xf0
                elif r is None and g is None and b is None:
                    # Mask out colors
                    write_mask |= 0x0f

            msg.append(write_mask)

            # Message terminator
            msg.append(0x0f)

        # send the message
        try:
            self._send_msg(msg)
        except socket.error:
            if retry:
                self.connect()
                self.set_rgbw(r, g, b, w, persist=persist, brightness=brightness,
                              retry=max(retry - 1, 0), w2=w2)

    @property
    def rgb(self):
        if self.mode != "color":
            return (255, 255, 255)
        red = self.raw_state[6]
        green = self.raw_state[7]
        blue = self.raw_state[8]
        return (red, green, blue)

    def set_rgb(self, r, g, b, persist=True, brightness=None, retry=2):
        self.set_rgbw(r, g, b, persist=persist, brightness=brightness,
                      retry=retry)

    def _calculate_brightness(self, rgb, level):
        r = rgb[0]
        g = rgb[1]
        b = rgb[2]
        hsv = colorsys.rgb_to_hsv(r, g, b)
        return colorsys.hsv_to_rgb(hsv[0], hsv[1], level)

    def _send_msg(self, bytes):
        # calculate checksum of byte array and add to end
        if self._use_csum:
            csum = sum(bytes) & 0xFF
            bytes.append(csum)
        with self._lock:
            self._socket.send(bytes)

    def _read_msg(self, expected):
        remaining = expected
        rx = bytearray()
        begin = time.time()
        while remaining > 0:
            if time.time() - begin > self.timeout:
                break
            try:
                with self._lock:
                    self._socket.setblocking(0)
                    chunk = self._socket.recv(remaining)
                    if chunk:
                        begin = time.time()
                    remaining -= len(chunk)
                    rx.extend(chunk)
            except socket.error:
                pass
            finally:
                self._socket.setblocking(1)
        return rx

    @property
    def clock(self):
        msg = bytearray([0x11, 0x1a, 0x1b, 0x0f])
        self._send_msg(msg)
        rx = self._read_msg(12)
        if len(rx) != 12:
            return
        year = rx[3] + 2000
        month = rx[4]
        date = rx[5]
        hour = rx[6]
        minute = rx[7]
        second = rx[8]
        # dayofweek = rx[9]
        try:
            dt = datetime.datetime(year, month, date, hour, minute, second)
        except:
            dt = None
        return dt

    def set_clock(self):
        msg = bytearray([0x10, 0x14])
        now = datetime.datetime.now()
        msg.append(now.year - 2000)
        msg.append(now.month)
        msg.append(now.day)
        msg.append(now.hour)
        msg.append(now.minute)
        msg.append(now.second)
        msg.append(now.isoweekday())  # day of week
        msg.append(0x00)
        msg.append(0x0f)
        self._send_msg(msg)

    def set_protocol(self, protocol):
        self.protocol = protocol.upper()

    def set_preset_pattern(self, pattern, speed=80):

        PresetPattern.valtostr(pattern)
        if not PresetPattern.valid(pattern):
            # print "Pattern must be between 0x25 and 0x38"
            raise Exception

        delay = utils.speed_to_delay(speed)
        # print "speed {}, delay 0x{:02x}".format(speed,delay)
        pattern_set_msg = bytearray([0x61])
        pattern_set_msg.append(pattern)
        pattern_set_msg.append(delay)
        pattern_set_msg.append(0x0f)

        self._send_msg(pattern_set_msg)

    @property
    def timers(self):
        msg = bytearray([0x22, 0x2a, 0x2b, 0x0f])
        self._send_msg(msg)
        resp_len = 88
        rx = self._read_msg(resp_len)
        if len(rx) != resp_len:
            print("response too short!")
            raise Exception

        # utils.dump_data(rx)
        start = 2
        timer_list = []
        # pass in the 14-byte timer structs
        for i in range(6):
            timer_bytes = rx[start:][:14]
            timer = LedTimer(timer_bytes)
            timer_list.append(timer)
            start += 14

        return timer_list

    def send_timers(self, timer_list):
        # remove inactive or expired timers from list
        for t in timer_list:
            if not t.isActive() or t.isExpired():
                timer_list.remove(t)

        # truncate if more than 6
        if len(timer_list) > 6:
            print("too many timers, truncating list")
            del timer_list[6:]

        # pad list to 6 with inactive timers
        if len(timer_list) != 6:
            for i in range(6 - len(timer_list)):
                timer_list.append(LedTimer())

        msg_start = bytearray([0x21])
        msg_end = bytearray([0x00, 0xf0])
        msg = bytearray()

        # build message
        msg.extend(msg_start)
        for t in timer_list:
            msg.extend(t.toBytes())
        msg.extend(msg_end)
        self._send_msg(msg)

        # not sure what the resp is, prob some sort of ack?
        rx = self._read_msg(1)
        rx = self._read_msg(3)

    def set_custom_pattern(self, rgb_list, speed, transition_type):
        # truncate if more than 16
        if len(rgb_list) > 16:
            print("too many colors, truncating list")
            del rgb_list[16:]

        # quit if too few
        if len(rgb_list) == 0:
            print("no colors, aborting")
            return

        msg = bytearray()

        first_color = True
        for rgb in rgb_list:
            if first_color:
                lead_byte = 0x51
                first_color = False
            else:
                lead_byte = 0
            r, g, b = rgb
            msg.extend(bytearray([lead_byte, r, g, b]))

        # pad out empty slots
        if len(rgb_list) != 16:
            for i in range(16 - len(rgb_list)):
                msg.extend(bytearray([0, 1, 2, 3]))

        msg.append(0x00)
        msg.append(utils.speed_to_delay(speed))

        if transition_type == "gradual":
            msg.append(0x3a)
        elif transition_type == "jump":
            msg.append(0x3b)
        elif transition_type == "strobe":
            msg.append(0x3c)
        else:
            # unknown transition string: using 'gradual'
            msg.append(0x3a)
        msg.append(0xff)
        msg.append(0x0f)

        self._send_msg(msg)

    def refresh_state(self):
        return self.update_state()


class BulbScanner(object):
    def __init__(self):
        self.found_bulbs = []

    def get_bulb_info_by_id(self, id):
        for b in self.found_bulbs:
            if b['id'] == id:
                return b
        return b

    def get_bulb_info(self):
        return self.found_bulbs

    def scan(self, timeout=10):

        DISCOVERY_PORT = 48899

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', DISCOVERY_PORT))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        msg = "HF-A11ASSISTHREAD".encode('ascii')

        # set the time at which we will quit the search
        quit_time = time.time() + timeout

        response_list = []
        # outer loop for query send
        while True:
            if time.time() > quit_time:
                break
            # send out a broadcast query
            sock.sendto(msg, ('<broadcast>', DISCOVERY_PORT))

            # inner loop waiting for responses
            while True:

                sock.settimeout(1)
                try:
                    data, addr = sock.recvfrom(64)
                except socket.timeout:
                    data = None
                    if time.time() > quit_time:
                        break

                if data is None:
                    continue
                if data == msg:
                    continue

                data = data.decode('ascii')
                data_split = data.split(',')
                if len(data_split) < 3:
                    continue
                item = dict()
                item['ipaddr'] = data_split[0]
                item['id'] = data_split[1]
                item['model'] = data_split[2]
                response_list.append(item)

        self.found_bulbs = response_list
        return response_list

