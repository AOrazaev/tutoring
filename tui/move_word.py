import curses

ESC_CODE = 27

def main(screen):
    curses.curs_set(0)
    curses.noecho()
    curses.start_color()

    max_y, max_x = screen.getmaxyx()
    text = 'MOVE_ME'
    y = max_y // 2
    x = max_x // 2 - len(text) // 2

    while True:
        screen.addstr(y, x, text)
        screen.refresh()

        ch = screen.getch()
        screen.addstr(y, x, len(text) * ' ')

        if ch == ESC_CODE:
            return
        elif ch == curses.KEY_LEFT:
            x = max(0, x - 1)
        elif ch == curses.KEY_RIGHT:
            x = min(max_x - len(text) - 1, x + 1)
        elif ch == curses.KEY_UP:
            y = max(0, y - 1)
        elif ch == curses.KEY_DOWN:
            y = min(max_y - 1, y + 1)

if __name__ == '__main__':
    curses.wrapper(main)
