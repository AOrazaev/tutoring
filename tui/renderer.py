import blessed
import re
from dataclasses import dataclass


def colored(text, rgb_fg=None, rgb_bg=None):
    bg_color = ""
    if rgb_bg:
        bg_color = f"\033[48;2;{rgb_bg[0]};{rgb_bg[1]};{rgb_bg[2]}m"

    fg_color = ""
    if rgb_fg:
        fg_color = f"\033[38;2;{rgb_fg[0]};{rgb_fg[1]};{rgb_fg[2]}m"

    reset_color = "\033[0m" if rgb_fg or rgb_bg else ""
    return fg_color + bg_color + text + reset_color


def strip_color(text: str) -> str:
    t = text.replace('\033[', 'ESCAPE033#')
    t = re.sub(r'ESCAPE033#48;2;\d+;\d+;\d+m', '', t)
    t = re.sub(r'ESCAPE033#38;2;\d+;\d+;\d+m', '', t)
    t = re.sub(r'ESCAPE033#0m', '', t)
    return t


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
        print(self.term.move_xy(x, y), end='')

    def clear(self):
        print(self.term.home + self.term.clear, end='')

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

    def draw_game_over(self, rgb_bg=None, rgb_fg=None):
        window = self.game_window
        text = 'GAME OVER'
        self._move(
            window.x + window.width * self.scale_x // 2 - len(text) // 2,
            window.y + window.height // 2
        )
        print(colored(text, rgb_bg=rgb_bg, rgb_fg=rgb_fg), end='', flush=True)

    def draw_text_center(self, text, rgb_bg=None, rgb_fg=None):
        window = self.game_window
        self._move(
            window.x + window.width * self.scale_x // 2 - len(text) // 2,
            window.y + window.height // 2
        )
        print(colored(text, rgb_bg=rgb_bg, rgb_fg=rgb_fg), end='', flush=True)

    def draw_text_below_border(self, text):
        window = self.game_window
        for i, row in enumerate(text.split('\n')):
            self._move(window.x, window.y + window.height + 2 + i)
            print(row, end='')

    def draw_text_above_border(self, text):
        window = self.game_window
        for i, row in enumerate(reversed(text.split('\n'))):
            self._move(window.x, window.y - 2 - i)
            print(row, end='')

    def draw_score(self, score):
        window = self.game_window
        text = f'Score: {score}'

        self._move(window.x, window.y - 2)
        print(text)
