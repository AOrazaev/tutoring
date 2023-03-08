import blessed


def main():
    term = blessed.Terminal()

    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        key = None
        while True:
            print(term.home + term.clear, end='')
            print('Press a key on a keyboard to see character\'s code')
            print('Press ESCAPE to exit')

            if key is not None:
                print(term.move_y(term.height // 2) +
                      term.center(
                          f'Key code is {key.code if key.code else ord(key)}'
                      ).rstrip())
            key = term.inkey()

            if key.code == term.KEY_ESCAPE:
                break


if __name__ == '__main__':
    main()
