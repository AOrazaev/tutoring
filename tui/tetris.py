import blessed
from snake import colored
from dataclasses import dataclass
from typing import List, Tuple
from tetris_pieces import (
    PATTERNS,
    TetrisPiece,
    rotate_clockwise,
    rotate_counterclockwise,
    piece_height,
    piece_width,
    pattern_rows,
)
import random
from datetime import datetime, timedelta


@dataclass
class MainWindow:
    x: int
    y: int
    width: int
    height: int


def create_centered_window(
    term: blessed.Terminal,
    width: int,
    height: int,
    scale_x: int
):
    return MainWindow(
        term.width//2 - (width * scale_x)//2,
        term.height//2 - height//2,
        width,
        height)


@dataclass
class GameField:
    filled: List[List[bool]]
    rendered_filled_part: List[List[str]]


class GameRenderer:
    def __init__(
            self,
            term: blessed.Terminal,
            width: int,
            height: int,
            scale_x: int = 2):
        self.term = term
        self.scale_x = scale_x
        self.game_window = create_centered_window(term, width, height, scale_x)

    def _move(self, x, y):
        print(term.move_xy(x, y), end='')

    def clear(self):
        print(term.home + term.clear, end='')

    def flush(self):
        print('', end='', flush=True)

    def draw_border(self):
        window = self.game_window
        self._move(window.x-1, window.y-1)
        print('┌' + '─' * window.width * self.scale_x + '┐', end='')
        for i in range(window.height):
            self._move(window.x-1, window.y + i)
            print('│' + ' ' * window.width * self.scale_x + '│', end='')
        self._move(window.x-1, window.y+window.height)
        print('└' + '─' * window.width * self.scale_x + '┘', end='')

    def render_field(
        self, piece: TetrisPiece, field: GameField
    ) -> List[List[str]]:
        copy = list(list(x) for x in field.rendered_filled_part)
        for y, (shift_x, row) in enumerate(self._piece_rows(piece)):
            for x, ch in enumerate(row):
                if piece.y + y <= 0:
                    continue
                copy[piece.y + y][piece.x + x + shift_x // self.scale_x] = ch
        return copy

    def draw(self, window: MainWindow):
        self.draw_border()

    # Tetris related
    def draw_field(self, field: GameField):
        window = self.game_window
        for y, row in enumerate(field.rendered_filled_part):
            self._move(window.x, window.y + y)
            print(''.join(row), end='')

    def draw_piece(self, piece: TetrisPiece):
        window = self.game_window
        for i, (shift_x, row) in enumerate(self._piece_rows(piece)):
            self._move(
                window.x + shift_x + piece.x * self.scale_x,
                window.y + piece.y + i)
            print(''.join(row), end='')

    def _piece_rows(self, piece):
        replace = {
            '.': '.' * self.scale_x,
            '#': colored(' ' * self.scale_x, rgb_bg=piece.pattern.rgb),
            '\n': '\n'
        }

        rows = [
           [replace[i] for i in row]
           for row in pattern_rows(piece.pattern)
        ]
        for r in rows:
            yield (
                len(''.join(r)) - len(''.join(r).lstrip('.')),
                [ch for ch in r if ch != '.'*self.scale_x]
            )


def can_move(piece: TetrisPiece, field: GameField) -> bool:
    # Out of left/right bounds
    if piece.x < 0 or piece.x + piece_width(piece) > len(field.filled[0]):
        return False

    # Hit the floor
    if piece.y + piece_height(piece) > len(field.filled):
        return False

    # Space is occupied
    for y, row in enumerate(pattern_rows(piece.pattern)):
        if piece.y + y < 0:
            continue
        for x, ch in enumerate(row):
            if ch == '#' and field.filled[piece.y + y][piece.x + x]:
                return False
    return True


def try_fix_piece(piece: TetrisPiece, field: GameField) -> bool:
    # Hit the top
    if piece.y < 0:
        return False

    # Set space to be occupied
    for y, row in enumerate(pattern_rows(piece.pattern)):
        for x, ch in enumerate(row):
            if ch == '#':
                field.filled[piece.y + y][piece.x + x] = True

    return True


def field_clenaup(field: GameField, renderer: GameRenderer) -> int:
    to_cleanup = []
    for i in reversed(range(len(field.filled))):
        if all(field.filled[i]):
            to_cleanup.append(i)

    for i in to_cleanup:
        del field.filled[i]
        del field.rendered_filled_part[i]

    field.filled = [
        [False for _ in range(len(field.filled[0]))]
        for __ in to_cleanup
    ] + field.filled

    field.rendered_filled_part = [
        [' '*renderer.scale_x for _ in range(len(field.filled[0]))]
        for __ in to_cleanup
    ] + field.rendered_filled_part

    return len(to_cleanup)


def init(term, width, height) -> Tuple[GameField, GameRenderer]:
    renderer = GameRenderer(term, width, height)
    field = GameField(
        [[False for _ in range(width)] for __ in range(height)],
        [[' '*renderer.scale_x for _ in range(width)] for __ in range(height)],
    )
    return field, renderer


def handle_key(
    key,
    piece: TetrisPiece,
    field: GameField
) -> Tuple[TetrisPiece, bool]:
    need_redraw = False

    if key.code == term.KEY_ESCAPE:
        exit(0)

    if key.code == term.KEY_LEFT:
        piece.x -= 1
        need_redraw = True

        if not can_move(piece, field):
            piece.x += 1
            need_redraw = False
        return piece, need_redraw

    if key.code == term.KEY_RIGHT:
        piece.x += 1
        need_redraw = True

        if not can_move(piece, field):
            piece.x -= 1
            need_redraw = False
        return piece, need_redraw

    if key.code == term.KEY_UP:
        rotated = rotate_counterclockwise(piece)
        if can_move(rotated, field):
            piece = rotated
            need_redraw = True
        return piece, need_redraw

    if key.code == term.KEY_DOWN:
        rotated = rotate_clockwise(piece)
        if can_move(rotated, field):
            piece = rotated
            need_redraw = True
        return piece, need_redraw


def main(term):
    field, renderer = init(term, 10, 20)
    CYCLE_TIME_SECONDS = 0.3
    need_redraw = True

    piece = TetrisPiece(4, 0, random.choice(PATTERNS))
    piece.y = -piece_height(piece)

    next_cycle = datetime.now() + timedelta(seconds=CYCLE_TIME_SECONDS)

    while True:
        if need_redraw:
            renderer.clear()
            renderer.draw_border()
            renderer.draw_field(field)
            renderer.draw_piece(piece)
            renderer.flush()

        time_left = (next_cycle - datetime.now()).total_seconds()
        if time_left > 0 and term.kbhit(timeout=time_left):
            key = term.inkey(esc_delay=0)
            piece, need_redraw = handle_key(key, piece, field)
            continue

        next_cycle = datetime.now() + timedelta(seconds=CYCLE_TIME_SECONDS)
        piece.y += 1
        need_redraw = True

        if not can_move(piece, field):
            piece.y -= 1

            # Update
            field.rendered_filled_part = renderer.render_field(piece, field)
            if not try_fix_piece(piece, field):
                return
            field_clenaup(field, renderer)

            piece = TetrisPiece(4, 0, random.choice(PATTERNS))
            piece.y = -piece_height(piece)


if __name__ == '__main__':
    term = blessed.Terminal()
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        main(term)
