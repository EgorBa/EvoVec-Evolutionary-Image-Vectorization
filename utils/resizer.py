import numpy as np
from PIL import Image

import config


def create_resized_image(png_path: str, max_w: int, max_h: int) -> str:
    im = Image.open(png_path).convert("RGB")
    (w, h) = im.size
    ratio = float(w) / float(h)

    new_w = min(w, max_w)
    new_h = new_w / ratio

    new_h = min(new_h, max_h)
    new_w = new_h * ratio

    if int(new_h) == h and int(new_w) == w:
        return png_path

    if config.DEBUG:
        print(f'Image has size ({w},{h}) that more than max ({config.MAX_W},{config.MAX_H}). '
              f'New size = ({int(new_w)},{int(new_h)})')
    im = im.resize((int(new_w), int(new_h)))
    im.save(config.RESIZED_PNG_PATH)
    return config.RESIZED_PNG_PATH


def resize_svg_file_data_to_init(png_path: str, svg_file_data: str) -> str:
    if png_path != config.RESIZED_PNG_PATH:
        return svg_file_data

    update_cache_if_need()
    (w, h) = config.PNG_IMAGE.size

    svg_file_data = svg_file_data.replace(f'width=\"{config.MAX_W}\"', f'width=\"{w}\"')
    svg_file_data = svg_file_data.replace(f'height=\"{config.MAX_H}\"', f'height=\"{h}\"')
    return svg_file_data


def resize_svg_file_data_from_init(png_path: str, svg_file_data: str) -> str:
    if png_path != config.RESIZED_PNG_PATH:
        return svg_file_data

    update_cache_if_need()
    (w, h) = config.PNG_IMAGE.size

    svg_file_data = svg_file_data.replace(f'width=\"{w}\"', f'width=\"{config.MAX_W}\"')
    svg_file_data = svg_file_data.replace(f'height=\"{h}\"', f'height=\"{config.MAX_H}\"')
    return svg_file_data


def update_cache_if_need():
    if config.PNG_IMAGE is None:
        config.PNG_IMAGE = np.array(Image.open(config.PNG_PATH).convert('RGB'), dtype=int)
