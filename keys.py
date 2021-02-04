#  import keys
#
#  a = keys.read()
#  if a == keys.UP:
#       


import sys, tty, termios

UP      = 0x90
DOWN    = 0x91
LEFT    = 0x92
RIGHT   = 0x93
QUIT    = 0xF0
TIMEOUT = 0xF1 

def read():
    ''' Read a single character from stdin with no buffering '''

    def getRaw():
        fd       = sys.stdin.fileno()
        tc_attrs = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, tc_attrs)
        return ch
    
    state = 0
    while True:
        ch = getRaw()
        if state == 0:
            if ord(ch) == 27:
                state = 1
            else:
                break
        elif state == 1:
            if ord(ch) == 91:
                state = 2
            else:
                break
        elif state == 2:
            if   ord(ch) == 65: return UP
            elif ord(ch) == 66: return DOWN
            elif ord(ch) == 67: return RIGHT
            elif ord(ch) == 68: return LEFT
            else:
                break

    return ch
