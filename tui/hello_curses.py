import curses

ESC_CODE = 27

def center_text(screen, text):
    max_y, max_x = screen.getmaxyx()
    screen.addstr(max_y // 2, max_x // 2 - len(text) // 2, text)

def main(screen):
    curses.curs_set(0)

    center_text(screen, "Hello Curses!")
    screen.refresh()
    screen.getch()

if __name__ == '__main__':
    curses.wrapper(main)
