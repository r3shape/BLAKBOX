from blakbox.globals import pg
from blakbox.atom import BOXatom

class BOXkeyboard(BOXatom):
    __slots__ = (
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
        "Num0",
        "Num1",
        "Num2",
        "Num3",
        "Num4",
        "Num5",
        "Num6",
        "Num7",
        "Num8",
        "Num9",
        "F1",
        "F2",
        "F3",
        "F4",
        "F5",
        "F6",
        "F7",
        "F8",
        "F9",
        "F10",
        "F11",
        "F12",
        "Space",
        "Escape",
        "Enter",
        "Tab",
        "Shift",
        "Ctrl",
        "Alt",
        "RShift",
        "RCtrl",
        "RAlt",
        "Up",
        "Down",
        "Left",
        "Right",
        "NumPad0",
        "NumPad1",
        "NumPad2",
        "NumPad3",
        "NumPad4",
        "NumPad5",
        "NumPad6",
        "NumPad7",
        "NumPad8",
        "NumPad9",
        "NumPadDivide",
        "NumPadMultiply",
        "NumPadSubtract",
        "NumPadAdd",
        "NumPadEnter",
        "NumPadDecimal",
        "LShift",
        "RShift",
        "LCtrl",
        "RCtrl",
        "LAlt",
        "RAlt",
        "LMeta",
        "RMeta",
        "LSuper",
        "RSuper",
        "CapsLock",
        "NumLock",
        "ScrollLock",
        "PrintScreen",
        "Pause",
        "Insert",
        "Delete",
        "Home",
        "End",
        "PageUp",
        "PageDown",
        "Grave",
        "Minus",
        "Equals",
        "LeftBracket",
        "RightBracket",
        "Backslash",
        "Semicolon",
        "Quote",
        "Comma",
        "Period",
        "Slash",
        "BackSpace",
        "Tab",
        "Enter",
        "Menu"
    )

    def __init__(self) -> None:
        super().__init__()

        self._unfreeze()
        # Letter keys
        self.A = pg.K_a
        self.B = pg.K_b
        self.C = pg.K_c
        self.D = pg.K_d
        self.E = pg.K_e
        self.F = pg.K_f
        self.G = pg.K_g
        self.H = pg.K_h
        self.I = pg.K_i
        self.J = pg.K_j
        self.K = pg.K_k
        self.L = pg.K_l
        self.M = pg.K_m
        self.N = pg.K_n
        self.O = pg.K_o
        self.P = pg.K_p
        self.Q = pg.K_q
        self.R = pg.K_r
        self.S = pg.K_s
        self.T = pg.K_t
        self.U = pg.K_u
        self.V = pg.K_v
        self.W = pg.K_w
        self.X = pg.K_x
        self.Y = pg.K_y
        self.Z = pg.K_z

        # Number keys
        self.Num0 = pg.K_0
        self.Num1 = pg.K_1
        self.Num2 = pg.K_2
        self.Num3 = pg.K_3
        self.Num4 = pg.K_4
        self.Num5 = pg.K_5
        self.Num6 = pg.K_6
        self.Num7 = pg.K_7
        self.Num8 = pg.K_8
        self.Num9 = pg.K_9

        # Function keys
        self.F1 = pg.K_F1
        self.F2 = pg.K_F2
        self.F3 = pg.K_F3
        self.F4 = pg.K_F4
        self.F5 = pg.K_F5
        self.F6 = pg.K_F6
        self.F7 = pg.K_F7
        self.F8 = pg.K_F8
        self.F9 = pg.K_F9
        self.F10 = pg.K_F10
        self.F11 = pg.K_F11
        self.F12 = pg.K_F12

        # Special keys
        self.Space = pg.K_SPACE
        self.Escape = pg.K_ESCAPE
        self.Enter = pg.K_RETURN
        self.Tab = pg.K_TAB
        self.Shift = pg.K_LSHIFT  # Left Shift
        self.Ctrl = pg.K_LCTRL    # Left Control
        self.Alt = pg.K_LALT      # Left Alt
        self.RShift = pg.K_RSHIFT  # Right Shift
        self.RCtrl = pg.K_RCTRL    # Right Control
        self.RAlt = pg.K_RALT      # Right Alt

        # Arrow keys
        self.Up = pg.K_UP
        self.Down = pg.K_DOWN
        self.Left = pg.K_LEFT
        self.Right = pg.K_RIGHT

        # Numpad keys
        self.NumPad0 = pg.K_KP0
        self.NumPad1 = pg.K_KP1
        self.NumPad2 = pg.K_KP2
        self.NumPad3 = pg.K_KP3
        self.NumPad4 = pg.K_KP4
        self.NumPad5 = pg.K_KP5
        self.NumPad6 = pg.K_KP6
        self.NumPad7 = pg.K_KP7
        self.NumPad8 = pg.K_KP8
        self.NumPad9 = pg.K_KP9
        self.NumPadDivide = pg.K_KP_DIVIDE
        self.NumPadMultiply = pg.K_KP_MULTIPLY
        self.NumPadSubtract = pg.K_KP_MINUS
        self.NumPadAdd = pg.K_KP_PLUS
        self.NumPadEnter = pg.K_KP_ENTER
        self.NumPadDecimal = pg.K_KP_PERIOD

        # Modifier keys
        self.LShift = pg.K_LSHIFT
        self.RShift = pg.K_RSHIFT
        self.LCtrl = pg.K_LCTRL
        self.RCtrl = pg.K_RCTRL
        self.LAlt = pg.K_LALT
        self.RAlt = pg.K_RALT
        self.LMeta = pg.K_LMETA
        self.RMeta = pg.K_RMETA
        self.LSuper = pg.K_LSUPER  # Windows key for left
        self.RSuper = pg.K_RSUPER  # Windows key for right

        # Miscellaneous keys
        self.CapsLock = pg.K_CAPSLOCK
        self.NumLock = pg.K_NUMLOCK
        self.ScrollLock = pg.K_SCROLLOCK
        self.PrintScreen = pg.K_PRINT
        self.Pause = pg.K_PAUSE
        self.Insert = pg.K_INSERT
        self.Delete = pg.K_DELETE
        self.Home = pg.K_HOME
        self.End = pg.K_END
        self.PageUp = pg.K_PAGEUP
        self.PageDown = pg.K_PAGEDOWN

        # Symbol keys
        self.Grave = pg.K_BACKQUOTE  # `~
        self.Minus = pg.K_MINUS      # -_
        self.Equals = pg.K_EQUALS    # =+
        self.LeftBracket = pg.K_LEFTBRACKET   # [{
        self.RightBracket = pg.K_RIGHTBRACKET # ]}
        self.Backslash = pg.K_BACKSLASH       # \|
        self.Semicolon = pg.K_SEMICOLON       # ;:
        self.Quote = pg.K_QUOTE               # '"
        self.Comma = pg.K_COMMA               # ,<
        self.Period = pg.K_PERIOD             # .>
        self.Slash = pg.K_SLASH               # /?
        self.BackSpace = pg.K_BACKSPACE
        self.Tab = pg.K_TAB
        self.Enter = pg.K_RETURN
        self.Menu = pg.K_MENU
        self._freeze()

class BOXmouse(BOXatom):
    __slots__ = (
        "_pos",
        "WheelUp",
        "Hovering",
        "WheelDown",
        "LeftClick",
        "WheelClick",
        "RightClick",
    )

    def __init__(self):
        super().__init__()
        
        self._unfreeze()
        self.WheelUp: int = 4
        self.WheelDown: int = 5
        self.LeftClick: int = 1
        self.WheelClick: int = 2
        self.RightClick: int = 3
        self.Hovering: type = None
        self._pos: list[list[int]] = [[0, 0] for _ in range(4)]
        self._freeze()
    
    @property
    def rel(self)-> list:
        return self._pos[0]
    
    @property
    def view(self)-> list:
        return self._pos[1]
    
    @property
    def world(self)-> list:
        return self._pos[2]
    
    @property
    def screen(self)-> list:
        return self._pos[3]
