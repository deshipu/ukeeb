import ukeeb
from ukeeb import HoldTap as HT
from micropython import const
import board
import adafruit_dotstar as dotstar
import time

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
  (          _Q, _W, _E, _R, _T, _Y, _U,  _I,  _O, _P),
  (          _A, _S, _D, _F, _G, _H, _J,  _K,  _L, _ENT),
  (HT(_LSH, _Z), _X, _C, _V, _B, _N, _M, _CM, _DT, HT(_RSH, _SL)),
  (HT(_LCT, _ESC), HT(_LSP, _TAB), HT(_LAL, _INS), HT(_L1, _PGDN), _BS,
    _SPC, HT(_L2, _PGUP), HT(_RAL, _DEL), HT(_RSP, _SC), HT(_RCT, _QT)),
), (
  (           _1,   _2,   _3,   _4,   _5,   _6,   _7,  _8,  _9,  _0),
  (          _F1,  _F2,  _F3,  _F4,  _F5,  _F6,  _MN, _EQ, _LB, _RB),
  (HT(_LSH, _F7),  _F8,  _F9, _F10, _F11, _F12, _BSL, _GR, _AU, _RSH),
  (         _LCT, _LSP, _LAL, _L1, _HOME, _END,  _L3, _AL, _AD, _AR),
), (
  (_LSH | _1,  _LSH | _2,  _LSH | _3,   _LSH | _4,   _LSH | _5,
   _LSH | _6,   _LSH | _7,  _LSH | _8,  _LSH | _9,  _LSH | _0),
  (_LAL | _F1, _LAL | _F2, _LAL | _F3,  _LAL | _F4,  _LAL | _F5,
   _LAL | _F6,  _LSH | _MN, _LSH | _EQ, _LSH | _LB, _LSH | _RB),
  (HT(_LSH, _LAL | _F7), _LAL | _F8, _LAL | _F9, _LAL | _F10, _LAL | _F11,
   _LAL | _F12, _LSH | _BSL, _LSH | _GR, _CAPS, _RSH),
  (_LCT, _LSP, _LAL, _L3, _HOME, _END, _L2, _RAL, _RSP, _RCT),
), (
  (  _Q, _W, _E, _R, _T, _Y, _U,  _I,  _O, _P),
  (  _A, _S, _D, _F, _G, _H, _J,  _K,  _L, _ENT),
  (_LSH, _X, _C, _V, _B, _N, _MT, _PP, _VU, _RSH),
  (_LCT, _LSP, _LAL, _L3, _RR, _FF, _L3, _PT, _VD, _NT),
)

COLS = (board.A6, board.A1, board.A4, board.A3, board.D6,
        board.SCL, board.SDA, board.D12, board.D10, board.D13)
ROWS = (board.MOSI, board.AREF, board.D11, board.D5)


class Keeb(ukeeb.Keeb):
    def __init__(self, matrix, cols, rows):
        super().__init__(matrix, cols, rows)
        self.leds = dotstar.DotStar(board.A5, board.A2, 40, brightness=0.1,
                                    auto_write=False)
        self.key_x = 0
        self.key_y = 0
        self.key_time = time.monotonic()

    def animate(self):
        i = 0
        y = 0
        dt = time.monotonic() - self.key_time
        for x in range(10):
            self.leds[i] = self.light(x, y, dt)
            i += 1
        y += 1
        for x in range(9, -1, -1):
            self.leds[i] = self.light(x, y, dt)
            i += 1
        y += 1
        for x in range(10):
            self.leds[i] = self.light(x, y, dt)
            i += 1
        y += 1
        for x in range(9, -1, -1):
            self.leds[i] = self.light(x, y, dt)
            i += 1
        self.leds.show()

    def light(self, x, y, dt):
        r2 = (x - self.key_x) ** 2 + (y - self.key_y) ** 2
        c = 255 - min(255, r2 * 30 + (dt * 10) ** 2)
        return min(c + self.current_layer * 100, 255), x * 25, min(255, y * 50)

    def press(self, x, y):
        super().press(x, y)
        self.key_x = x
        self.key_y = y
        self.key_time = time.monotonic()
