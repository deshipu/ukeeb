import digitalio
import usb_hid
import time


class HoldTap:
    def __init__(self, hold, tap):
        self.hold = hold
        self.tap = tap


class Layer:
    def __init__(self, layer):
        self.layer = layer


class Keeb:
    def __init__(self, matrix, cols, rows):
        self.matrix = matrix
        self.cols = [digitalio.DigitalInOut(pin) for pin in cols]
        self.rows = [digitalio.DigitalInOut(pin) for pin in rows]
        for col in self.cols:
            col.switch_to_output(value=0)
        for row in self.rows:
            row.switch_to_input(pull=digitalio.Pull.DOWN)
        self.keyboard_device = None
        self.media_device = None
        for device in usb_hid.devices:
            if device.usage == 0x06 and device.usage_page == 0x01:
                self.keyboard_device = device
            if device.usage == 0x01 and device.usage_page == 0x0c:
                self.media_device = device
        if not self.keyboard_device:
            raise RuntimeError("no HID keyboard device")
        self.debounce = bytearray(len(cols))
        self.last_state = bytearray(len(cols))
        self.current_layer = 0
        self.pressed_keys = set()
        self.last_held = None
        self.release_next = None

    def animate(self):
        pass

    def scan(self):
        if self.release_next:
            try:
                self.pressed_keys.remove(self.release_next)
            except KeyError:
                pass
            self.release_next = None
        for x, col in enumerate(self.cols):
            col.value = 1
            debounce_bits = 0
            for y, row in enumerate(self.rows):
                state = row.value
                debounce_bits |= state << y
                if state != bool(self.debounce[x] & (1 << y)):
                    continue
                last_state = bool(self.last_state[x] & (1 << y))
                if state:
                    self.last_state[x] |= 1 << y
                else:
                    self.last_state[x] &= ~(1 << y)
                if state == last_state:
                    continue
                if state:
                    self.press(x, y)
                    self.key_x = x
                    self.key_y = y
                    self.key_time = time.monotonic()
                else:
                    self.release(x, y)
            col.value = 0
            self.debounce[x] = debounce_bits

    def press(self, x, y):
        if self.last_held:
            self.last_held = None
        key = self.matrix[self.current_layer][y][x]
        if isinstance(key, HoldTap):
            self.last_held = key
            key = key.hold
        if isinstance(key, Layer):
            self.current_layer = key.layer
            return
        if key < 0:
            self.send_media_report(-key)
            return
        self.pressed_keys.add(key)

    def release_all(self, x, y):
        for layer in self.matrix:
            key = layer[y][x]
            if not key:
                continue
            if isinstance(key, HoldTap):
                key = key.hold
            if isinstance(key, Layer):
                self.current_layer = 0
                continue
            if key < 0:
                self.send_media_report(0)
                continue
            try:
                self.pressed_keys.remove(key)
            except KeyError:
                pass

    def release(self, x, y):
        key = self.matrix[self.current_layer][y][x]
        if self.last_held == key:
            self.release_all(x, y)
            self.pressed_keys.add(key.tap)
            self.release_next = key.tap
            self.last_held = None
            return
        self.release_all(x, y)

    def send_report(self, pressed_keys):
        report = bytearray(8)
        report_mod_keys = memoryview(report)[0:1]
        report_no_mod_keys = memoryview(report)[2:]
        keys = 0
        for code in pressed_keys:
            if code == 0:
                continue
            if code & 0xff00:
                report_mod_keys[0] |= (code & 0xff00) >> 8
            if code & 0x00ff and keys < 6:
                report_no_mod_keys[keys] = code & 0x00ff
                keys += 1
        self.keyboard_device.send_report(report)

    def send_media_report(self, code):
        if not self.media_device:
            return
        report = bytearray(2)
        report[0] = code
        self.media_device.send_report(report)

    def run(self):
        last_pressed_keys = set()
        anim_delay = 0
        while True:
            self.scan()
            if self.pressed_keys != last_pressed_keys:
                self.send_report(self.pressed_keys)
                last_pressed_keys = set(self.pressed_keys)
            anim_delay += 1
            if anim_delay > 7:
                self.animate()
                anim_delay = 0
