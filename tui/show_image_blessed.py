"""
Usage:
    show_image_blessed.py <image_path>
"""
import blessed
from PIL import Image
from docopt import docopt


def colored(text, rgb_fg=None, rgb_bg=None):
    bg_color = ""
    if rgb_bg:
        bg_color = f"\033[48;2;{rgb_bg[0]};{rgb_bg[1]};{rgb_bg[2]}m"

    fg_color = ""
    if rgb_fg:
        fg_color = f"\033[48;2;{rgb_fg[0]};{rgb_fg[1]};{rgb_fg[2]}m"

    reset_color = "\033[0m"
    return fg_color + bg_color + text + reset_color


def generate_text_image(term, im):
    timg = []
    for y in range(im.height):
        def pixel_text(x):
            rgb = im.getpixel((x, y))
            return colored('  ', rgb_bg=rgb)
        timg.append(''.join(pixel_text(x) for x in range(im.width)))
    return '\n'.join(timg)


def draw_img(term, im):
    print(term.home)
    print(generate_text_image(term, im))

def show_img(im, max_size=(40, 40)):
    im.thumbnail(max_size)
    im = im.quantize(colors=32).convert(mode='RGB')

    term = blessed.Terminal()
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        draw_img(term, im)
        term.inkey()


if __name__ == '__main__':
    opts = docopt(__doc__)

    with Image.open(opts['<image_path>']) as im:
        show_img(im)
