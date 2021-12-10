import board
import ukeeb
from ukeeb import HoldTap as HT
from micropython import const
import rotaryio
import analogio
import digitalio
import usb_hid

ROWS = (board.D9, board.RX, board.TX, board.A5, board.A2)
COLS = (board.D14, board.LED, board.MISO, board.SCK, board.MOSI, board.D6,
        board.D5, board.D11, board.D13, board.D10, board.D12, board.SDA,
        board.SCL)

_A = const(4)
_B = const(5)
_C = const(6)
_D = const(7)
_E = const(8)
_F = const(9)
_G = const(10)
_H = const(11)
_I = const(12)
_J = const(13)
_K = const(14)
_L = const(15)
_M = const(16)
_N = const(17)
_O = const(18)
_P = const(19)
_Q = const(20)
_R = const(21)
_S = const(22)
_T = const(23)
_U = const(24)
_V = const(25)
_W = const(26)
_X = const(27)
_Y = const(28)
_Z = const(29)

_1 = const(30)
_2 = const(31)
_3 = const(32)
_4 = const(33)
_5 = const(34)
_6 = const(35)
_7 = const(36)
_8 = const(37)
_9 = const(38)
_0 = const(39)

_ENT = const(40) # Enter
_ESC = const(41) # Esc
_BS = const(42)  # Backspace
_TAB = const(43) # Tab
_SPC = const(44) # Space
_MN = const(45) # Minus -/_
_EQ = const(46) # Equal =/+
_LB = const(47) # Left bracket [/{
_RB = const(48) # Right bracket ]/}
_BSL = const(49) # Backslash \/|
_SC = const(51) # Semicolon ;/:
_QT = const(52) # Quote '/"
_GR = const(53) # Grave `/~
_CM = const(54) # Comma ,/<
_DT = const(55) # Dot ./>
_SL = const(56) # Slash //?
_CAPS = const(57) # Caps lock

_F1 = const(58)
_F2 = const(59)
_F3 = const(60)
_F4 = const(61)
_F5 = const(62)
_F6 = const(63)
_F7 = const(64)
_F8 = const(65)
_F9 = const(66)
_F10 = const(67)
_F11 = const(68)
_F12 = const(69)

_PS = const(70) # Print screen
_SCL = const(71) # Scroll lock
_PA = const(72) # Pause

_INS = const(73) # Insert
_HOME = const(74) # Home
_PGUP = const(75) # Page up
_DEL = const(76) # Delete
_END = const(77) # End
_PGDN = const(78) # Page down
_AR = const(79) # Arrow right
_AL = const(80) # Arrow left
_AD = const(81) # Arrow down
_AU = const(82) # Arrow up

_APP = const(101) # Menu

_LCT = const(0x0100) # Left control
_LSH = const(0x0200) # Left shift
_LAL = const(0x0400) # Left alternate
_LSP = const(0x0800) # Left super
_RCT = const(0x1000) # Right control
_RSH = const(0x2000) # Right shift
_RAL = const(0x4000) # Right alternate
_RSP = const(0x8000) # Right super

_FN = ukeeb.Layer(1)

_MT = const(-226) # Mute
_VU = const(-233) # Volume up
_VD = const(-234) # Volume down

_RR = const(-179) # Rewind
_FF = const(-180) # Fast forward
_NT = const(-181) # Next track
_PT = const(-182) # Prev track
_ST = const(-183) # Stop track
_PP = const(-205) # Play/pause


MATRIX = (
    (_GR,  _1, _2, _3, _4, _5,   _6, _7,  _8,  _9, _0,  _MN,  _EQ),
    (_ESC, _Q, _W, _E, _R, _T,   _Y, _U,  _I,  _O, _P,  _BSL, _BS),
    (_TAB, _A, _S, _D, _F, _G,   _H, _J,  _K,  _L, _SC, _QT,  _ENT),
    (_LSH, _Z, _X, _C, _V, _B,   _N, _M, _CM, _DT, _SL, _AU,  _RSH),
    (_LCT, _LSP, _LB, _RB, _LAL, _FN,
     _SPC, _RAL, _INS, _DEL, _AL, _AD, _AR),
), (
    (_APP,  _F1, _F2, _F3, _F4, _F5, _F6, _F7, _F8, _F9, _F10, _MN, _EQ),
    (_ESC,  _PP, _VU, _MT, _R, _T, _Y, _U, _I, _F11, _F12, _BSL, _BS),
    (_CAPS, _NT, _VD, _NT, _F, _G, _H, _J, _K, _L, _SC, _QT,  _ENT),
    (_LSH, _Z, _X, _C, _V, _B,  _N, _M, _CM, _DT, _SL, _PGUP, _RSH),
    (_RCT, _RSP, _PS, _DEL, _LAL, _FN,
     _SPC, _RAL, _LB, _RB, _HOME, _PGDN, _END),
),

class Keeb(ukeeb.Keeb):
    def __init__(self, matrix, cols, rows):
        super().__init__(matrix, cols, rows)
        self.knob = rotaryio.IncrementalEncoder(board.AREF, board.A1)
        for device in usb_hid.devices:
            if device.usage == 0x02 and device.usage_page == 0x01:
                break
        else:
            raise RuntimeError("no HID mouse device")
        self.mouse_device = device
        self.mx = analogio.AnalogIn(board.A3)
        self.my = analogio.AnalogIn(board.A4)
        self.lmb = digitalio.DigitalInOut(board.A0)
        self.lmb.switch_to_input(pull = digitalio.Pull.UP)
        self.rmb = digitalio.DigitalInOut(board.A6)
        self.rmb.switch_to_input(pull = digitalio.Pull.UP)
        self.mouse_move = False
        self.last_knob = 0

    def send_mouse_report(self):
        report = bytearray(4)
        report[0] = ((not self.lmb.value) << 0) | ((not self.rmb.value) << 1)
        knob = self.knob.position
        if self.last_knob != knob:
            report[3] = max(-127, min(127, knob - self.last_knob)) & 0xff
        self.last_knob = knob

        x = self.mx.value - 0x7fff - 500
        y = 0x7fff - self.my.value + 500
        if x * x + y * y > 4000 * 4000:
            if x > 0:
                x = max(0, x - 3800)
            else:
                x = min(0, x + 3800)
            if y > 0:
                y = max(0, y - 3800)
            else:
                y = min(0, y + 3800)
            report[1] = min(max(-127, x >> 10), 127) & 0xff
            report[2] = min(max(-127, y >> 10), 127) & 0xff
        else:
            report[2] = 0
            report[1] = 0
        if report[0] or report[1] or report[2] or report[3]:
            self.mouse_move = False
            self.mouse_device.send_report(report)
        elif not self.mouse_move:
            self.mouse_move = True
            self.mouse_device.send_report(report)

    def animate(self):
        self.send_mouse_report()
