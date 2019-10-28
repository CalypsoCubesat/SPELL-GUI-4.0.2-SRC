import sys

UP = '-up-'
DOWN = '-down-'
LEFT = '-left-'
RIGHT = '-right-'
ESC = '-esc-'
ENTER = '-enter-'
TAB = '-tab-'

################################################################################
class _Getch:
    """
    Gets a single character from standard input.  Does not echo to the
    screen.
    """
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()

################################################################################
class _GetchCommon:

    scanCode = False 

    def echo(self, ch):
        o = ord(ch)
        if self.scanCode:
            if o==75:
                result = LEFT
            elif o==77:
                result =  RIGHT
            elif o==72:
                result =  UP
            elif o==80:
                result =  DOWN
            else:
                result = ch
        else:
            if o==13 or o==10:
                sys.stdout.write('\n')
                result = ENTER
            elif o==9:
                sys.stdout.write('\t')
                result = TAB
            elif o==27:
                result = ESC
            else:
                sys.stdout.write(ch)
                result = ch
        self.scanCode = False
        return result

################################################################################
class _GetchUnix(_GetchCommon):
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            o = ord(ch)
            if (o == 0) or (o == 224):
                self.scanCode = True
                ch = sys.stdin.read(1)
            ch = self.echo(ch)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


################################################################################
class _GetchWindows(_GetchCommon):
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        ch = msvcrt.getch()
        o = ord(ch)
        if (o == 0) or (o == 224):
            self.scanCode = True
            ch = msvcrt.getch()
        ch = self.echo(ch)
        return ch


getch = _Getch()