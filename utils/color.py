import os

import numpy as np
from cairosvg import svg2png

import config
from dto.svg_picture import SvgPicture
from tqdm import tqdm

from utils.image import get_area
from fitness.loss import read_images


def fix_init_colors(picture: SvgPicture):
    path_tmp_svg = os.path.join(config.TMP_FOLDER, f'tmp.svg')
    path_tmp_png = os.path.join(config.TMP_FOLDER, f'tmp.png')
    picture.save_as_svg(path_tmp_svg)
    with open(path_tmp_svg, 'r') as f:
        svg_str = f.read()
        svg2png(svg_str, write_to=str(path_tmp_png))
    cur_im, init_im = read_images(path_tmp_png, picture.png_init_path)
    os.remove(path_tmp_svg)
    os.remove(path_tmp_png)

    c = 0
    set_no_equal_colors = set()
    for i in range(picture.height):
        for j in range(picture.width):
            sum_diff = 0
            for k in range(3):
                sum_diff += abs(cur_im[i][j][k] - init_im[i][j][k])
            if sum_diff > config.COLOR_DIFF:
                c += 1
                if not set_no_equal_colors.__contains__(cur_im[i][j].tostring()):
                    set_no_equal_colors.add(cur_im[i][j].tostring())
    print(f'total pixels = {picture.width * picture.height}, got not equals pixels = {c}')
    for p in tqdm(picture.paths):
        if set_no_equal_colors.__contains__(p.colors[0].tostring()):
            small_pic = SvgPicture([p], picture.png_init_path)

            path_tmp_svg = os.path.join(config.TMP_FOLDER, f'tmp.svg')
            path_tmp_png = os.path.join(config.TMP_FOLDER, f'tmp.png')
            small_pic.save_as_svg(path_tmp_svg)
            with open(path_tmp_svg, 'r') as f:
                svg_str = f.read()
                svg2png(svg_str, write_to=str(path_tmp_png))
            cur_im, init_im = read_images(path_tmp_png, picture.png_init_path)
            os.remove(path_tmp_svg)
            os.remove(path_tmp_png)

            map_count_of_init_color = {}
            path_area = get_area(p.path_arr, small_pic.width, small_pic.height)

            for i in range(int(path_area.y0), int(path_area.y1)):
                for j in range(int(path_area.x0), int(path_area.x1)):
                    if cur_im[i][j][0] == 0 and cur_im[i][j][1] == 0 and cur_im[i][j][2] == 0:
                        pass
                    else:
                        init_key_color = init_im[i][j].tostring()
                        if not map_count_of_init_color.keys().__contains__(init_key_color):
                            map_count_of_init_color[init_key_color] = 0
                        map_count_of_init_color[init_key_color] += 1
            if len(map_count_of_init_color.keys()) > 0:
                best_color = p.colors[0].tostring
                pix_count = 0
                for k in map_count_of_init_color.keys():
                    if map_count_of_init_color[k] > pix_count:
                        pix_count = map_count_of_init_color[k]
                        best_color = k
                p.colors[0] = np.fromstring(best_color, dtype=int)
