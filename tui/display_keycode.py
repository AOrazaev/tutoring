import curses
from hello_curses import center_text

ESC_CODE = 27

def safe_character_display(ch_code):
    if ch_code == ord('\n'):
        return '\\n'
    if ch_code == ord('\t'):
        return '\\t'
    return chr(ch_code)

def main(screen):
    curses.curs_set(0)
    curses.noecho()

    screen.addstr("Key listener app.\n")
    screen.addstr("Press any key to see it's code.\n")
    screen.addstr("Press Esc to exit.\n")

    while True:
        ch_code = screen.getch()
        if ch_code == ESC_CODE:
            break
        screen.deleteln()
        center_text(
            screen,
            f"You pressed '{safe_character_display(ch_code)}' the code of this character is: {ch_code}"
        )
        screen.refresh()


if __name__ == '__main__':
    curses.wrapper(main)
