import blessed
import random
import audio

from dataclasses import dataclass
from renderer import GameRenderer, colored, strip_color
from typing import List


EMPTY = ' '
BOMB = colored("M", rgb_bg=(100, 0, 0))
FLAG = colored("F", rgb_bg=(0, 0, 255))
WIDTH = 30
HEIGHT = 15
NUM_BOMBS = WIDTH * HEIGHT // 13

TOP_TEXT = '''
MINESWEEPER:

Open all cells with no mine to win.
If you step on a mine - you loose.
'''

INSTRUCTIONS = '''
Arrow keys - to move.
Space - to open a cell.
f - to flag a cell.
ESC - to exit.
'''.strip('\n')


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass
class MinsweeperState:
    cursor: Point
    field: List[List[str]]
    is_opened: List[List[bool]]
    is_flagged: List[List[bool]]
    game_over: bool
    victory: bool


class MinsweeperRenderer(GameRenderer):
    def __init__(self, *args, **kwargs):
        super(MinsweeperRenderer, self).__init__(*args, **kwargs)

    def _get_ch_by_xy(self, state: MinsweeperState, xy: Point):
        if state.is_flagged[xy.y][xy.x]:
            return FLAG
        if state.is_opened[xy.y][xy.x]:
            return state.field[xy.y][xy.x]
        return colored('.', rgb_bg=(30, 30, 30))

    def draw_field(self, state: MinsweeperState):
        for y in range(self.game_window.height):
            for x in range(self.game_window.width):
                self._move(self.game_window.x + x, self.game_window.y + y)
                print(self._get_ch_by_xy(state, Point(x=x, y=y)), end='')

    def draw_cursor(self, state: MinsweeperState):
        ch = strip_color(self._get_ch_by_xy(state, state.cursor))
        self._move(
            self.game_window.x + state.cursor.x,
            self.game_window.y + state.cursor.y
        )
        print(colored(ch, rgb_bg=(150, 150, 150)), end='')


def open_around(state: MinsweeperState):
    to_visit = [
        xy for xy in xy_around(state.cursor)
        if state.field[xy.y][xy.x] != BOMB
    ]
    seen = set(to_visit)
    seen.add(state.cursor)

    while to_visit:
        next = to_visit.pop()
        state.is_opened[next.y][next.x] = True
        if state.field[next.y][next.x] != EMPTY:
            continue

        for p in xy_around(next):
            if p in seen or state.field[p.y][p.x] == BOMB:
                continue

            to_visit.append(p)
            seen.add(p)


def xy_around(p: Point):
    for delta_y in (-1, 0, 1):
        for delta_x in (-1, 0, 1):
            if delta_x == 0 and delta_y == 0:
                continue

            if delta_x + p.x < 0 or delta_x + p.x >= WIDTH:
                continue

            if delta_y + p.y < 0 or delta_y + p.y >= HEIGHT:
                continue

            yield Point(x=p.x+delta_x, y=p.y+delta_y)


def num_bombs_around(field: List[List[str]], p: Point) -> int:
    n = 0
    for xy in xy_around(p):
        if field[xy.y][xy.x] == BOMB:
            n += 1
    return n


def generate_hints(field: List[List[str]]):
    for y in range(len(field)):
        for x in range(len(field[0])):
            if field[y][x] == EMPTY:
                n = num_bombs_around(field, Point(x=x, y=y))
                if n > 0:
                    field[y][x] = str(n)


def generate_field(width, height, num_bombs) -> List[List[str]]:
    field = [[EMPTY for _ in range(width)] for __ in range(height)]
    n = 0
    while n < num_bombs:
        x, y = random.randrange(width), random.randrange(height)
        if field[y][x] == BOMB:
            continue
        field[y][x] = BOMB
        n += 1

    generate_hints(field)
    return field


def check_win(state: MinsweeperState):
    for y in range(len(state.field)):
        for x in range(len(state.field[y])):
            if state.field[y][x] == BOMB:
                continue
            if not state.is_opened[y][x]:
                return False
    return True


def handle_key(key, state: MinsweeperState):
    if key.code == term.KEY_ESCAPE:
        exit(0)

    if state.game_over:
        return

    if key.code == term.KEY_LEFT:
        state.cursor = Point(x=max(state.cursor.x - 1, 0), y=state.cursor.y)

    if key.code == term.KEY_RIGHT:
        state.cursor = Point(
                x=min(state.cursor.x + 1, WIDTH - 1),
                y=state.cursor.y
                )

    if key.code == term.KEY_UP:
        state.cursor = Point(x=state.cursor.x, y=max(state.cursor.y - 1, 0))

    if key.code == term.KEY_DOWN:
        state.cursor = Point(
                x=state.cursor.x,
                y=min(state.cursor.y + 1, HEIGHT - 1)
                )

    if state.victory:
        return

    if key == 'f':
        if state.is_opened[state.cursor.y][state.cursor.x]:
            return

        state.is_flagged[state.cursor.y][state.cursor.x] = (
                not state.is_flagged[state.cursor.y][state.cursor.x]
                )

    if key == ' ':
        if state.is_flagged[state.cursor.y][state.cursor.x]:
            return

        state.is_opened[state.cursor.y][state.cursor.x] = True

        if state.field[state.cursor.y][state.cursor.x] == BOMB:
            state.game_over = True
            audio.play("audio/arcade_explosion.wav")

        if check_win(state):
            state.victory = True
            audio.play("audio/bonus_collected.mp3")

        if state.field[state.cursor.y][state.cursor.x] == EMPTY:
            open_around(state)


def main(term):

    renderer = MinsweeperRenderer(term, WIDTH, HEIGHT, 1)
    state = MinsweeperState(
        cursor=Point(x=WIDTH//2, y=HEIGHT//2),
        field=generate_field(WIDTH, HEIGHT, NUM_BOMBS),
        is_opened=[[False for _ in range(WIDTH)] for __ in range(HEIGHT)],
        is_flagged=[[False for _ in range(WIDTH)] for __ in range(HEIGHT)],
        game_over=False,
        victory=False
    )

    while True:
        renderer.draw_border()
        renderer.draw_field(state)
        renderer.draw_cursor(state)
        renderer.draw_text_above_border(TOP_TEXT)
        renderer.draw_text_below_border(INSTRUCTIONS)

        if state.game_over:
            renderer.draw_text_center(
                "!!! GAME OVER !!!", rgb_bg=(200, 0, 0), rgb_fg=(0, 0, 0))

        if state.victory:
            renderer.draw_text_center(
                "!!! VICTORY !!!", rgb_bg=(0, 200, 0), rgb_fg=(0, 0, 0))

        renderer.flush()

        handle_key(term.inkey(), state)


if __name__ == '__main__':
    term = blessed.Terminal()
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        main(term)
