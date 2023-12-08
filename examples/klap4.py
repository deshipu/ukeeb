import ukeeb
from ukeeb import HoldTap as HT
from microcontroller import pin
from micropython import const
import board
import trackpad
import busio
import usb_hid

ROWS = (pin.PA03, pin.PA04, pin.PA07, pin.PA06, pin.PA27)
COLS = (pin.PA30, pin.PA31, pin.PA00, pin.PA01, pin.PA02, pin.PA05,
        pin.PA16, pin.PA17, pin.PA18, pin.PA19, pin.PA22, pin.PA23)

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

_L1 = ukeeb.Layer(1)
_L2 = ukeeb.Layer(2)
_L3 = ukeeb.Layer(3)

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
  ( 0, _Q, _W, _E, _R, _T, _Y, _U, _I,  _O,  _P, 0),
  (_Q, _A, _S, _D, _F, _G, _H, _J, _K, _L, _QT, _P),
  (_LCT, _Z, _X, _C, _V, _B, _N, _M, _CM, _DT, _SL, _LAL),
  (_LSH, _LCT, _LAL, _LSP, 0, _LCT, _LAL, 0, 0, 0, _AU, 0),
  (_LSH, HT(_LSP, _APP), _LSP, HT(_RSH, _ESC), HT(_L1, _TAB), _BS,
    _SPC, HT(_L2, _ENT), HT(_RAL, _DEL), _AL, _AD, _AR)
), (
  (0, _LSH|_1, _LSH|_2, _LSH|_3, _LSH|_4, _LSH|_5,
   _LSH|_6, _LSH|_7, _LSH|_8, _LSH|_9, _LSH|_0, 0),
  (_LSH|_1, _1, _2, _3, _4, _5, _6, _7, _8, _9, _0, _LSH|_0),
  (_LCT, _PS, _LAL|_F4, _CAPS, _GR, _BSL, _MN, _EQ, _LB, _RB, _SC, _LAL),
  (_LSH, _LCT, _LAL, _LSP, 0, _LCT, _LAL, 0, 0, 0, _PGUP, 0),
  (_LSH, _LSP, _LSP, _LSP,  _L1, _L2,
   _LSH|_INS, _L3, HT(_RAL, _INS), _HOME, _PGDN, _END)
), (
  (0, _F1, _F2, _F3, _F4, _F5, _F6, _F7, _F8, _F9, _F10, 0),
  (_F1, _F11, _HOME, _PGDN, _PGUP, _END, _AL, _AD, _AU, _AR, _F12, _F10),
  (_LCT, _VD, _VU, _MT, _LSH|_GR, _LSH|_BSL,
   _LSH|_MN, _LSH|_EQ, _LSH|_LB, _LSH|_RB, _LSH|_SC, _LAL),
  (_LSH, _LCT, _LAL, _LSP, 0, _LCT, _LAL, 0, 0, 0, _LCT|_AU, 0),
  (_LSH, _LSP, _LSP, _LSH, _L3, _LCT|_BS,
   _L1, _L2, _LCT|_INS, _LCT|_AL, _LCT|_AD, _LCT|_AR)
), (
  (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
  (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
  (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
  (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
  (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
),

class Keeb(ukeeb.Keeb):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            i2c = busio.I2C(pin.PA09, pin.PA08)
            i2c.try_lock()
            i2c.scan()
            i2c.unlock()
        except RuntimeError:
            self.trackpad = None
            return
        for device in usb_hid.devices:
            if device.usage == 0x02 and device.usage_page == 0x01:
                break
        else:
            return
        self.mouse_device = device
        self.trackpad = trackpad.Trackpad(i2c)

    def animate(self):
        if self.trackpad is None:
            return
        while self.trackpad.available():
            data = self.trackpad.read()
            data[0] &= 0x07
            if data[1]:
                data[1] ^= 0xff
            self.mouse_device.send_report(data)
