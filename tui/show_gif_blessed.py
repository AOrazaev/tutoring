"""
Usage:
    show_image_blessed.py <image_path> [--max-size=<max-size>]
"""
import blessed
from PIL import Image, ImageSequence
from docopt import docopt
import time


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


def show_gif(im, max_size=(70, 70)):
    term = blessed.Terminal()
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        frames = collect_frames(term, im, max_size)
        i = 0
        while True:
            print(term.home + frames[i % len(frames)])
            time.sleep(0.15)
            i += 1

def collect_frames(term, im, max_size):
    frames = []
    for fr in ImageSequence.Iterator(im):
        rgb_im = fr.convert(mode='RGB')
        rgb_im.thumbnail(max_size, Image.Resampling.NEAREST) #Image.Resampling.LANCZOS)
        frames.append(generate_text_image(term, rgb_im))
    return frames

if __name__ == '__main__':
    opts = docopt(__doc__)
    sz = 40
    if opts['--max-size']:
        sz = int(opts['--max-size'])

    with Image.open(opts['<image_path>']) as im:
        show_gif(im, max_size=(sz, sz))
