import blessed
import random

from dataclasses import dataclass
from renderer import GameRenderer, colored
from typing import List


WIDTH = 30
HEIGHT = 30

TOP_TEXT = '''GAME OF LIFE'''

INSTRUCTIONS = '''R - to restart. ESC - to exit'''


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass
class GameOfLifeState:
    cells: List[List[bool]]
    width: int
    height: int


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


def generate_random_state(
    width: int, height: int, chance_alive: float = 0.3
) -> GameOfLifeState:
    cells = [
        [random.random() > (1 - chance_alive) for _x in range(width)]
        for _y in range(height)
    ]
    return GameOfLifeState(cells, width, height)


class GameOfLifeRenderer(GameRenderer):
    def __init__(self, *args, **kwargs):
        super(GameOfLifeRenderer, self).__init__(*args, **kwargs)

    def draw_state(self, state: GameOfLifeState):
        for i, row in enumerate(state.cells):
            s = ''.join((
                ' ' if not alive else colored(' ', rgb_bg=(200, 200, 200))
            ) * self.scale_x for alive in row)
            self._move(self.game_window.x, self.game_window.y + i)
            print(s, end='')


def count_neighbours(state: GameOfLifeState, p: Point) -> int:
    count = 0
    for xy in xy_around(p):
        count += state.cells[xy.y][xy.x]

    return count


def next_cell(is_alive: bool, num_neighbors: int) -> bool:
    if is_alive and num_neighbors in (2, 3):
        return True

    if not is_alive and num_neighbors == 3:
        return True

    return False


def next_generation(state: GameOfLifeState):
    num_neighbors = [
        [
            count_neighbours(state, Point(x=x, y=y))
            for x in range(state.width)
        ]
        for y in range(state.height)
    ]
    state.cells = [
        [
            next_cell(state.cells[y][x], num_neighbors[y][x])
            for x in range(state.width)
        ]
        for y in range(state.height)
    ]


def handle_key(term, key, state: GameOfLifeState) -> GameOfLifeState:
    if key.code == term.KEY_ESCAPE:
        exit(0)

    if key == 'r':
        return generate_random_state(WIDTH, HEIGHT)

    return state


def main(term):
    renderer = GameOfLifeRenderer(term, WIDTH, HEIGHT)
    state = generate_random_state(WIDTH, HEIGHT)

    while True:
        renderer.clear()
        renderer.draw_border()
        renderer.draw_state(state)
        renderer.draw_text_above_border(TOP_TEXT)
        renderer.draw_text_below_border(INSTRUCTIONS)
        renderer.flush()

        if term.kbhit(timeout=0.1):
            state = handle_key(term, term.inkey(), state)

        next_generation(state)


if __name__ == '__main__':
    term = blessed.Terminal()
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        main(term)
