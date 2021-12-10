import keypad


class KeebHalf:
    def __init__(self, uart, cols, rows):
        self.matrix = uart
        self.keypad = keypad.KeyMatrix(rows, cols)
        self.width = len(cols)
        self.buf = bytearray(1)
        self.uart = uart

    def scan(self):
        event = keypad.Event()
        while self.keypad.events:
            self.keypad.events.get_into(event)
            y, x = divmod(event.key_number, self.width)
            if event.pressed:
                self.press(x, y)
            else:
                self.release(x, y)

    def press(self, x, y):
        self.buf[0] = x | (y << 4) | 128
        self.uart.write(self.buf)

    def release(self, x, y):
        self.buf[0] = x | (y << 4)
        self.uart.write(self.buf)

    def run(self):
        while True:
            self.scan()


    def read_uart(self):
        while self.uart.in_waiting:
            self.uart.readinto(self.buf)
            x = self.buf[0] & 0x0f
            y = (self.buf[0] & 0x70) >> 4
            if self.buf[0] & 0x80:
                self.press(9 - x, y)
            else:
                self.release(9 - x, y)
