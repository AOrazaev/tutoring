#!/usr/bin/env python3
"""
Usage:
    show_image.py <image_path>
"""
from PIL import Image
from docopt import docopt
import curses


COLOR_DICT = {}
next_color_id = 10

SCREEN = ''

def restore_colors_wrapper(func):
    def wrapper(*args, **kwargs):
        saved_colors = []
        for i in range(1, curses.COLORS):
            saved_colors.append(curses.color_content(i))

        try:
            func(*args, **kwargs)
        finally:
            for i, rgb in zip(range(1, curses.COLORS), saved_colors):
                curses.init_color(i, *rgb)

    return wrapper

def create_color(r, g, b):
    global SCREEN
    global next_color_id
    try:
        curses.init_color(
            next_color_id,
            r * 1000 // 256,
            g * 1000 // 256,
            b * 1000 // 256
        )
    except:
        raise Exception(str(["init_color", next_color_id, r, g, b, COLOR_DICT]))
    COLOR_DICT[(r, g, b)] = next_color_id
    next_color_id += 1
    return next_color_id - 1


def get_color(r, g, b):
    if (r, g, b) not in COLOR_DICT:
        create_color(r, g, b)
    return COLOR_DICT[(r, g, b)]


BRUSH_DICT = {}
next_pair_id = 1


def create_style(fg_color, bg_color):
    global next_pair_id

    try:
        curses.init_pair(next_pair_id, fg_color, bg_color)
    except:
        raise Exception(str(["init_pair", next_pair_id, fg_color, bg_color]))

    style = curses.color_pair(next_pair_id)
    next_pair_id += 1
    return style


def get_brush(r, g, b):
    if (r, g, b) not in COLOR_DICT:
        BRUSH_DICT[(r, g, b)] = create_style(
            curses.COLOR_BLACK,
            get_color(r, g, b)
        )
    return BRUSH_DICT[(r, g, b)]


def addstr_colored(screen, y, x, text, rgb_fg=None, rgb_bg=None):
    bg_color = ""
    if rgb_bg:
        bg_color = f"\033[48;2;{rgb_bg[0]};{rgb_bg[1]};{rgb_bg[2]}mHello\033[0m"

    fg_color = ""
    if rgb_fg:
        fg_color = f"\033[48;2;{rgb_fg[0]};{rgb_fg[1]};{rgb_fg[2]}mHello\033[0m"

    reset_color = "\033[0m"
    screen.addstr(y, x, fg_color + bg_color + text + reset_color)

def show_img(screen, im, max_size=(60, 40)):
    global SCREEN
    SCREEN = screen
    im.thumbnail(max_size)
    im = im.quantize(colors=32).convert(mode='RGB')
    for y in range(im.height):
        for x in range(im.width):
            rgb = im.getpixel((x, y))
            addstr_colored(screen, y, x, ' ', rgb_bg=rgb)
            break
            #screen.addstr(y, x, ' ', get_brush(*rgb))

    screen.refresh()
    screen.getch()


if __name__ == '__main__':
    opts = docopt(__doc__)

    def wrap(screen):
        curses.curs_set(0)
        curses.noecho()
        screen.keypad(True)
        with Image.open(opts['<image_path>']) as im:
            show_img(screen, im)

    curses.wrapper(wrap)
