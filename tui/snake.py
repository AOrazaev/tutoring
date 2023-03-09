import blessed
import random
import audio


def colored(text, rgb_fg=None, rgb_bg=None):
    bg_color = ""
    if rgb_bg:
        bg_color = f"\033[48;2;{rgb_bg[0]};{rgb_bg[1]};{rgb_bg[2]}m"

    fg_color = ""
    if rgb_fg:
        fg_color = f"\033[48;2;{rgb_fg[0]};{rgb_fg[1]};{rgb_fg[2]}m"

    reset_color = "\033[0m"
    return fg_color + bg_color + text + reset_color


def draw_border(term, width, height, x, y):
    print(term.move_xy(x, y) + '┌' + '─'*width * 2 + '┐')
    for i in range(height):
        print(term.move_xy(x, y + i + 1) + '│' + ' '*width * 2 + '│')
    print(term.move_xy(x, y + i + 2) + '└' + '─' * width*2 + '┘')


def draw_snake(game_field, snake):
    text = colored('##', rgb_bg=(0, 255, 0))
    for x, y in snake:
        print(term.move_xy(game_field['x'] + x*2, game_field['y'] + y) + text)


def draw_berry(game_field, x, y):
    text = colored('##', rgb_bg=(255, 0, 0))
    print(term.move_xy(game_field['x'] + x*2, game_field['y'] + y) + text)


def draw_score(game_field, score):
    print(term.move_xy(game_field['x'], game_field['y']-2) + f'Score: {score}')


def new_berry(game_field, snake):
    x, y = snake[0]
    while (x, y) in snake:
        x = random.randrange(game_field['width'])
        y = random.randrange(game_field['height'])

    return (x, y)


def main(term):
    direction = (0, 0)
    SPEED_Y = 1
    SPEED_X = 1
    DELAY = 0.1

    game_field = {
        'x': term.width // 2 - 40 + 1,
        'y': term.height // 2 - 20 + 1,
        'width': 40,
        'height': 40
    }

    x = game_field['width'] // 2
    y = game_field['height'] // 2

    snake = [(x, y)]
    berry_xy = new_berry(game_field, snake)
    score = 0

    while True:
        x = min(max(-1, snake[-1][0]+direction[0]), game_field['width'])
        y = min(max(-1, snake[-1][1]+direction[1]), game_field['height'])

        # check end game
        if x == -1 or y == -1:
            return
        if x == game_field['width'] or y == game_field['height']:
            return
        if direction != (0, 0) and (x, y) in snake:
            return

        snake.append((x, y))

        # check if we ate a berry
        if (x, y) == berry_xy:
            audio.play('audio/bite_an_apple.mp3')
            score += 100
            berry_xy = new_berry(game_field, snake)
        else:
            del snake[0]

        # drawing
        print(term.home + term.clear, end='')
        draw_border(
            term,
            game_field['width'],
            game_field['height'],
            game_field['x'] - 1,
            game_field['y'] - 1
        )
        draw_snake(game_field, snake)
        draw_berry(game_field, *berry_xy)
        draw_score(game_field, score)

        # keyboard handling
        if term.kbhit(timeout=DELAY):
            key = term.inkey(esc_delay=0)
            if key.code == term.KEY_ESCAPE:
                return

            if key.code == term.KEY_LEFT and direction[0] == 0:
                direction = (-SPEED_X, 0)
            elif key.code == term.KEY_RIGHT and direction[0] == 0:
                direction = (SPEED_X, 0)
            elif key.code == term.KEY_UP and direction[1] == 0:
                direction = (0, -SPEED_Y)
            elif key.code == term.KEY_DOWN and direction[1] == 0:
                direction = (0, SPEED_Y)


if __name__ == '__main__':
    term = blessed.Terminal()
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        main(term)
