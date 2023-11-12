from pathlib import Path

import numpy as np
from svgtrace import trace
import os
from svgpathtools import svg2paths, Line, QuadraticBezier
from PIL import Image
import time

import config
from dto.svg_path import SvgPath
from dto.svg_picture import SvgPicture
from dto.svg_segment import M, C

THISDIR = str(Path(__file__).resolve().parent)


def complex_to_pair(n):
    data = str(n).split('+')
    if len(data) == 1:
        data = str(n).split('-')
    if len(data) == 1:
        if data[0].__contains__("j"):
            return 0, round(float(data[0][:-1]), 1)
        else:
            return round(float(data[0]), 1), 0
    return round(float(data[0][1:]), 1), round(float(data[1][:-2]), 1)


def get_color(color) -> np.array:
    c = str(color).split(",")
    color_array = np.array([int(c[0][4:]), int(c[1]), int(c[2][:-1])])
    return color_array


def preprocess_svg_paths(svg_path, png_file_path: str, w: int, h: int) -> SvgPicture:
    width, height = Image.open(png_file_path).size
    paths, attributes = svg2paths(svg_file_location=svg_path)
    new_paths = []
    for path, attr in zip(paths, attributes):
        if float(attr['opacity']) < 0.7:
            continue
        new_curve = []
        is_first = True
        last_coord = None
        for curve in path:
            if is_first:
                is_first = False
                p1, p2 = complex_to_pair(curve.start)
                new_curve.append(M(p1, p2))
            if isinstance(curve, Line):
                p1, p2 = complex_to_pair(curve.start)
                p3, p4 = complex_to_pair(curve.end)

                if last_coord is not None and (p1 != last_coord[0] or p2 != last_coord[1]):
                    new_curve.append(M(p1, p2))

                new_curve.append(C(p1, p2, p3, p4, p3, p4))
                last_coord = p3, p4
            elif isinstance(curve, QuadraticBezier):
                p1, p2 = complex_to_pair(curve.start)
                p3, p4 = complex_to_pair(curve.end)
                p5, p6 = complex_to_pair(curve.control)

                if last_coord is not None and (p1 != last_coord[0] or p2 != last_coord[1]):
                    new_curve.append(M(p1, p2))

                new_curve.append(C(p1, p2, p5, p6, p3, p4))
                last_coord = p3, p4
            else:
                print(f'unkhown curve = {curve}')
        new_paths.append(SvgPath(path_arr=new_curve, width=width, height=height, colors=[get_color(attr['fill'])]))
    return SvgPicture(new_paths, png_file_path)


def get_initial_svg(png_file_path) -> SvgPicture:
    start_time = time.time()
    svg_path = os.path.join(THISDIR, f"tmp.svg")
    png_path = os.path.join(THISDIR, png_file_path)
    Path(svg_path).write_text(trace(png_path), encoding="utf-8")
    w, h = Image.open(png_path).size
    svg_pic = preprocess_svg_paths(svg_path, png_path, w, h)
    os.remove(svg_path)
    if config.DEBUG:
        print('Algo vectorization time =', round(abs(time.time() - start_time), 3), 'sec', ', paths count =',
              len(svg_pic.paths))
    return svg_pic

# For test
# get_initial_svg(os.path.join("data", "img_3.png")).save_as_svg("lolkek.svg")
