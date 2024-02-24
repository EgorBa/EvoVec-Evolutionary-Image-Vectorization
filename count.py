import os

import numpy as np
from PIL import Image
from cairosvg import svg2png
from svgpathtools import svg2paths


def image_diff_mse(png_first, png_second) -> float:
    image_first, image_second = read_images(png_first, png_second)
    return float(np.sum(np.power((abs(image_second - image_first) / 255), 2)))


def with_bg(path):
    image = Image.open(path).convert('RGBA')
    new_image = Image.new('RGBA', (image.width, image.height), (255, 255, 255, 255))
    new_image.paste(image, (0, 0), image)
    new_image.save(path, "PNG")
    return Image.open(path).convert('RGBA')


def read_images(png_first, png_second):
    r = Image.open(png_first).convert('RGBA')
    image_first = np.array(r, dtype=int)
    image_second = np.array(with_bg(png_second).resize((r.width, r.height)), dtype=int)
    return image_first, image_second


dir = "data/test images"

live = os.path.join(dir, "live")
init = os.path.join(dir, "init")
i = 0

for i in sorted(os.listdir(live)):
    path_png_tmp = os.path.join(live, i)
    if i.__contains__(".png"):
        os.remove(path_png_tmp)

for image_svg, image_png in zip(sorted(os.listdir(live)), sorted(os.listdir(init))):
    print(image_svg)
    path_svg = os.path.join(live, image_svg)
    path_png_tmp = os.path.join(live, f'{image_svg}.png')
    path_png = os.path.join(init, image_png)
    print(path_svg)
    print(path_png)
    paths, attributes = svg2paths(svg_file_location=path_svg)
    print(f' count of paths = {len(paths)}')

    with open(path_svg, 'r') as f:
        svg_str = f.read()
        svg2png(svg_str, write_to=str(path_png_tmp))
    f = image_diff_mse(path_png, path_png_tmp)
    print(f'fitness = {f}')

    # os.remove(path_png_tmp)
