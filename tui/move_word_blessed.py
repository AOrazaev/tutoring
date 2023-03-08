import blessed


def main(term):
    text = 'MOVE_ME'
    x = term.width // 2 - len(text) // 2
    y = term.height // 2

    while True:
        print(term.home + term.clear + term.move_xy(x, y) + text)

        key = term.inkey()
        if key.code == term.KEY_ESCAPE:
            return

        if key.code == term.KEY_LEFT:
            x = max(x-1, 0)
        elif key.code == term.KEY_RIGHT:
            x = min(x+1, term.width - len(text))
        elif key.code == term.KEY_UP:
            y = max(y-1, 0)
        elif key.code == term.KEY_DOWN:
            y = min(y+1, term.height - 2)


if __name__ == '__main__':
    term = blessed.Terminal()
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        main(term)
