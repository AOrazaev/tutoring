import curses
import time

ESC_CODE = 27

def main(screen):
    curses.curs_set(0)
    curses.noecho()
    curses.start_color()
    screen.nodelay(True)

    max_y, max_x = screen.getmaxyx()
    text = 'MOVE_ME'
    y = max_y // 2
    x = max_x // 2 - len(text) // 2

    speed = (0, 0)
    while True:
        if speed[0] or speed[1]:
            screen.addstr(y, x, len(text) * ' ')
            y += speed[0]
            x += speed[1]
            y = max(0, min(max_y - 1, y))
            x = max(0, min(max_x - len(text) - 1, x))

        screen.addstr(y, x, text)
        screen.refresh()
        time.sleep(0.05)

        ch = screen.getch()
        if ch == ESC_CODE:
            return
        elif ch == curses.KEY_LEFT:
            speed = (0, -1)
        elif ch == curses.KEY_RIGHT:
            speed = (0, 1)
        elif ch == curses.KEY_UP:
            speed = (-1, 0)
        elif ch == curses.KEY_DOWN:
            speed = (1, 0)

if __name__ == '__main__':
    curses.wrapper(main)
