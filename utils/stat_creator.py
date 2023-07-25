import math
import os.path

from PIL import Image
from PIL import ImageDraw
from cairosvg import svg2png
import matplotlib.pyplot as plt

import config


def create_gif(gif_name):
    frames = []
    step = math.ceil(config.STEP_EVOL / 1000)

    for i in range(0, config.STEP_EVOL):
        frame_number = i * step
        if frame_number >= config.STEP_EVOL:
            break
        path_tmp_svg = os.path.join(config.TMP_FOLDER, f'gen_{frame_number}.svg')
        path_tmp_png = os.path.join(config.TMP_FOLDER, f'gen_{frame_number}.png')
        with open(path_tmp_svg, 'r') as f:
            svg_str = f.read()
            svg2png(svg_str, write_to=str(path_tmp_png))
        frame = Image.open(path_tmp_png)
        img = ImageDraw.Draw(frame)
        img.text((10, 10), f'gen : {frame_number}', fill=(0, 0, 0))
        frames.append(frame)

    frames[0].save(
        gif_name,
        save_all=True,
        append_images=frames[1:],
        optimize=True,
        duration=10,
        loop=0
    )


def create_graf(data, graf_name):
    x = []
    y = []
    for (x1, y1) in data:
        x.append(x1)
        y.append(y1)

    plt.plot(x, y)
    plt.xlabel("population number", fontsize=14)
    plt.ylabel("fitness function", fontsize=14)
    plt.savefig(graf_name)


def get_gen_file_paths_by_numbers(numbers):
    ans_paths = []
    for n in numbers:
        path_tmp_svg = os.path.join(config.TMP_FOLDER, f'gen_{n}.svg')
        path_tmp_png = os.path.join(config.TMP_FOLDER, f'gen_{n}.png')
        with open(path_tmp_svg, 'r') as f:
            svg_str = f.read()
            svg2png(svg_str, write_to=str(path_tmp_png))
        ans_paths.append(path_tmp_png)
    return ans_paths
