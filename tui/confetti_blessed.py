import blessed
import time
import random


def draw_confetti(term, n, styles):
    print(term.home + term.clear)
    for _ in range(n):
        color = random.choice(styles)
        print(term.move_xy(
            random.randrange(term.width),
            random.randrange(term.height)
        ) + color(' '))


def main():
    term = blessed.Terminal()

    styles = [
        term.on_color_rgb(0, 0, 256),
        term.on_color_rgb(256, 0, 0),
        term.on_color_rgb(0, 256, 0),
    ]

    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        while True:
            draw_confetti(term, 150, styles)
            time.sleep(0.5)


if __name__ == '__main__':
    main()
