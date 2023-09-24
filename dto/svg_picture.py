from typing import List
import drawsvg as draw
from cairosvg import svg2png
import typing
import cv2
import os

import config
from dto.svg_path import SvgPath
from utils.image import read_picture, get_contours
from utils.loss import opt_transport_loss, image_diff, image_diff_exp
from PIL import Image


class SvgPicture:
    paths: List[SvgPath] = []
    fitness: float = 0.0
    png_cnt: typing.Sequence[cv2.UMat]
    width: int
    height: int
    paths_count: int
    png_init_path: str

    def __init__(self, list_of_paths: List[SvgPath], png_init_path: str):
        if config.FITNESS_TYPE == config.Fitness.OPT_TRANSPORT:
            png_pic = read_picture(png_init_path)
            self.png_cnt = get_contours(png_pic)
        self.paths = list_of_paths
        self.paths_count = len(self.paths)
        width, height = Image.open(png_init_path).size
        self.width = width
        self.height = height
        self.png_init_path = png_init_path

    def __copy__(self):
        paths = []
        for path in self.paths:
            paths.append(path.__copy__())
        return SvgPicture(paths, self.png_init_path)

    def save_as_svg(self, filepath_svg: str):
        picture = draw.Drawing(self.width, self.height)
        for path in self.paths:
            picture.append(path.create_drawing_object())
        picture.save_svg(filepath_svg)

    def culc_fitness_function(self, clear_after=True):
        path_tmp_svg = os.path.join(config.TMP_FOLDER, f'tmp.svg')
        path_tmp_png = os.path.join(config.TMP_FOLDER, f'tmp.png')
        self.save_as_svg(path_tmp_svg)
        with open(path_tmp_svg, 'r') as f:
            svg_str = f.read()
            svg2png(svg_str, write_to=str(path_tmp_png))

        if config.FITNESS_TYPE == config.Fitness.IMAGE_DIFF:
            self.fitness = image_diff(self.png_init_path, path_tmp_png)
        elif config.FITNESS_TYPE == config.Fitness.OPT_TRANSPORT:
            cur_pic = read_picture(path_tmp_png)
            cur_cnt = get_contours(cur_pic)
            self.fitness = opt_transport_loss(self.png_cnt, cur_cnt)
        elif config.FITNESS_TYPE == config.Fitness.IMAGE_DIFF_EXP:
            self.fitness = image_diff_exp(self.png_init_path, path_tmp_png)

        if clear_after:
            os.remove(path_tmp_svg)
            os.remove(path_tmp_png)

        return self.fitness
