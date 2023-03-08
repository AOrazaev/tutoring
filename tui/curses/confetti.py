import curses
import time
import random


next_pair_id = 1

def create_style(fg_color, bg_color):
    global next_pair_id

    curses.init_pair(next_pair_id, fg_color, bg_color)
    style = curses.color_pair(next_pair_id)
    next_pair_id += 1
    return style


def main(screen):
    curses.curs_set(0)
    curses.noecho()
    curses.start_color()

    colors = [
        create_style(curses.COLOR_WHITE, curses.COLOR_BLUE),
        create_style(curses.COLOR_WHITE, curses.COLOR_RED),
        create_style(curses.COLOR_WHITE, curses.COLOR_YELLOW)
    ]

    max_y, max_x = screen.getmaxyx()
    N = 150

    while True:
        screen.clear()

        for _ in range(N):
            try:
                screen.addstr(
                    random.randrange(max_y),
                    random.randrange(max_x),
                    ' ',
                    random.choice(colors)
                )
            except:
                pass

        screen.refresh()
        time.sleep(0.6)


if __name__ == '__main__':
    curses.wrapper(main)
