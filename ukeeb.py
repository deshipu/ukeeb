import usb_hid
import keypad


class HoldTap:
    """
    A special behavior, that lets you send a modifier when a key
    is held, or a scan code when it is tapped.
    """
    def __init__(self, hold, tap):
        self.hold = hold
        self.tap = tap
        self.layer = 0


class Layer:
    """
    A special behavior that lets you switch layers.
    """
    def __init__(self, layer):
        self.layer = layer


class Keeb:
    """The main class representing the keyboard itself."""


    def __init__(self, matrix, cols, rows):
        """
        Creates a keyboard. ``matrix`` is a tuple of tuples of
        tuples defining the layers, rows and individual key scan
        codes, modifiers or special keys. ``cols`` and ``rows`` are
        tuples of DigitalInOut defining the pins of the matrix.
        """

        self.matrix = matrix
        self.keypad = keypad.KeyMatrix(rows, cols)
        self.width = len(cols)
        self.keyboard_device = None
        self.media_device = None
        for device in usb_hid.devices:
            if device.usage == 0x06 and device.usage_page == 0x01:
                self.keyboard_device = device
            if device.usage == 0x01 and device.usage_page == 0x0c:
                self.media_device = device
        if not self.keyboard_device:
            raise RuntimeError("no HID keyboard device")
        self.current_layer = 0
        self.pressed_keys = set()
        self.last_held = None
        self.release_next = None

    def animate(self):
        """Override this to do something on every animation frame."""

    def scan(self):
        """
        Scan the matrix and call ``press`` and ``release`` to update
        the ``pressed_keys`` attribute and handle other behaviors.
        Called continuously from the main loop.
        """
        if self.release_next:
            try:
                self.pressed_keys.remove(self.release_next)
            except KeyError:
                pass
            self.release_next = None
        event = keypad.Event()
        while self.keypad.events:
            self.keypad.events.get_into(event)
            y, x = divmod(event.key_number, self.width)
            if event.pressed:
                self.press(x, y)
            else:
                self.release(x, y)

    def animate(self):
        """Override this to do something on every animation frame."""

    def press(self, x, y):
        """Called when a keys is pressed."""

        if self.last_held:
            self.last_held = None
        key = self.matrix[self.current_layer][y][x]
        if isinstance(key, HoldTap):
            self.last_held = key
            self.last_held.layer = self.current_layer
            key = key.hold
        if isinstance(key, Layer):
            self.current_layer = key.layer
            return
        if key < 0:
            self.send_media_report(-key)
            return
        self.pressed_keys.add(key)

    def release_all(self, x, y):
        """A helper to make sure keys from all layers are released."""

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
        """Called when a key is released."""

        self.release_all(x, y)
        if (self.last_held and
                self.last_held == self.matrix[self.last_held.layer][y][x]):
            self.pressed_keys.add(self.last_held.tap)
            self.release_next = self.last_held.tap
            self.last_held = None

    def send_report(self, pressed_keys):
        """Sends the USB HID keyboard report."""

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
        """Sends the USB HID media report."""

        if not self.media_device:
            return
        report = bytearray(2)
        report[0] = code
        self.media_device.send_report(report)

    def run(self):
        """Runs the main loop."""

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
