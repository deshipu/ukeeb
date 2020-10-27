import board
import ukeeb
from micropython import const


ROWS = (board.RX, board.TX, board.A5, board.A2, board.A3)
COLS = (board.MISO, board.SCK, board.MOSI, board.D6, board.A0, board.AREF,
        board.D9, board.D5, board.D11, board.D13, board.D10, board.D12,
        board.SDA, board.SCL) # board.D14
LEDS = (board.A4,)
STICK = (board.A6, board.A2)

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
_ASH = const(50) # # ~
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

_DIV = const(84)
_MUL = const(85)
_SUB = const(86)
_ADD = const(87)
_NEN = const(88)
_DOT = const(90)

_N1 = const(89) # Numpad 1
_N2 = const(90) # Numpad 2
_N3 = const(91) # Numpad 3
_N4 = const(92) # Numpad 4
_N5 = const(93) # Numpad 5
_N6 = const(94) # Numpad 6
_N7 = const(95) # Numpad 7
_N8 = const(96) # Numpad 8
_N9 = const(97) # Numpad 9
_N0 = const(98) # Numpad 0

_APP = const(101) # Menu
_PWR = const(102)

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
 ( _GR,  _1,  _2,  _3, _4,  _5,  _6,  _7,  _8,  _9,  _0,  _MN,  _EQ,  _BS),
 (_TAB,  _Q,  _W,  _E, _R,  _T,  _Y,  _U,  _I,  _O,  _P,  _LB,  _RB, _BSL),
 (_CAPS, _A,  _S,  _D, _F,  _G,  _H,  _J,  _K,  _L, _SC,  _QT, _ENT,    0),
 (_LSH,  _Z,  _X,  _C, _V,  _B,  _N,  _M, _CM, _DT, _SL, _RSH,  _AU, _INS),
 (_ESC,_LCT,_LSP,_L1,_LAL,_SPC,_SPC,_RAL,_DEL,_RCT,   0,  _AL,  _AD,  _AR),
), (
 (_PT, _F1, _F2, _F3, _F4, _F5,   _F6, _F7, _F8, _F9,  _F10, _F11,  _F12, _BS),
 (_NT, _VU,   0,   0,   0,   0,   _N7, _N8, _N9, _SUB, _DIV, _MUL,     0,   0),
 (_MT, _VD,   0,   0,   0,   0,   _N4, _N5, _N6, _ADD,    0,    0,  _ENT,   0),
 (_LSH,_PP,   0, _PS,_SCL, _PA,   _N1, _N2, _N3, _NEN,    0, _RSH, _PGUP,_INS),
 (_ESC,_LCT,_APP,_L1,_LAL,_SPC,   _N0,_DOT,_DOT, _RCT,    0,_HOME, _PGDN,_END),
),

ukeeb.Keeb(MATRIX, COLS, ROWS).run()
