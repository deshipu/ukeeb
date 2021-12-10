import board
import ukeeb
from ukeeb import HoldTap as HT
from micropython import const
import analogio
import digitalio
import usb_hid

ROWS = (board.A3, board.A1, board.A4)
COLS = (board.AREF, board.A0, board.D6, board.MOSI, board.SCK, board.MISO,
        board.A2, board.A5, board.TX, board.RX, board.D9, board.D5)

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
  (   _Q, _A, _W, _E, _R, _T, _Y, _U, _I,  _O,  _QT, _P),
  ( _TAB, HT(_LSH, _Z), _S, _D, _F, _G,
   _H, _J, _K,  _L,  HT(_RSH, _SL), _ENT),
  (HT(_L1, _DEL), _ESC, HT(_LSP, _X), HT(_LAL, _C), HT(_LCT, _V), HT(_RAL, _B),
   HT(_RAL, _N), HT(_RCT, _M), HT(_LAL, _CM), HT(_RSP, _DT), _SPC, HT(_L2, _BS)),
), (
  (_F1, _1, _F2, _F3, _F4, _F5, _F6, _F7, _F8, _F9, _0, _F10),
  (_CAPS, _BSL, _2, _3, _4, _5, _6, _7, _8, _9, _SC, _INS),
  (_L3, _L2, _AL, _AD, _AU, _AR, _MN, _EQ, _LB, _RB, _L2, _L3),
), (
  (_GR, _LSH|_1, _LSH|_GR, 0, _LAL|_F4, _PP,
   _VD, _VU, _MT, _LAL|_F11, _LSH|_0, _LAL|_F12),
  (_LAL|_TAB, _LSH|_BSL, _LSH|_2, _LSH|_3, _LSH|_4, _LSH|_5,
   _LSH|_6, _LSH|_7, _LSH|_8, _LSH|_9, _SC, _INS),
  (_L3, _L1, _HOME, _PGDN, _PGUP, _END,
   _LSH|_MN, _LSH|_EQ, _LSH|_LB, _LSH|_RB, _L1, _L3),
), (
  (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
  (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
  (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
),

Keeb = ukeeb.Keeb
