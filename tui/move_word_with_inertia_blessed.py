import blessed


def main(term):
    text = 'MOVE_ME'
    direction = (0, 0)
    SPEED_Y = 1
    SPEED_X = 2

    x = term.width // 2 - len(text) // 2
    y = term.height // 2

    while True:
        x = min(max(0, x+direction[0]), term.width - len(text))
        y = min(max(0, y+direction[1]), term.height - 2)

        print(term.home + term.clear + term.move_xy(x, y) + text)

        if term.kbhit(timeout=0.1):
            key = term.inkey(esc_delay=0)
            if key.code == term.KEY_ESCAPE:
                return

            if key.code == term.KEY_LEFT:
                direction = (-SPEED_X, 0)
            elif key.code == term.KEY_RIGHT:
                direction = (SPEED_X, 0)
            elif key.code == term.KEY_UP:
                direction = (0, -SPEED_Y)
            elif key.code == term.KEY_DOWN:
                direction = (0, SPEED_Y)


if __name__ == '__main__':
    term = blessed.Terminal()
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        main(term)
