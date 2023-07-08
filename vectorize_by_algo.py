from pathlib import Path
from svgtrace import trace
import numpy as np
import os
from svgpathtools import svg2paths, Line, QuadraticBezier
from PIL import Image
import time

import config
from dto.svg_path import SvgPath
from dto.svg_picture import SvgPicture

THISDIR = str(Path(__file__).resolve().parent)


def complex_to_pair(n):
    data = str(n).split('+')
    if len(data) == 1:
        data = str(n).split('-')
    if len(data) == 1:
        if data[0].__contains__("j"):
            return 0, float(data[0][:-1])
        else:
            return float(data[0]), 0
    return float(data[0][1:]), float(data[1][:-2])


def preprocess_svg_paths(svg_path, png_file_path: str) -> SvgPicture:
    width, height = Image.open(png_file_path).size
    paths, attributes = svg2paths(svg_file_location=svg_path)
    new_paths = []
    for path, attr in zip(paths, attributes):
        if attr['opacity'] != '1':
            continue
        new_curve = []
        is_first = True
        for curve in path:
            if is_first:
                is_first = False
                p1, p2 = complex_to_pair(curve.start)
                new_curve.append(p1)
                new_curve.append(p2)
            if isinstance(curve, Line):
                p1, p2 = complex_to_pair(curve.end)
                new_curve.append(p1)
                new_curve.append(p2)
                new_curve.append(p1)
                new_curve.append(p2)
                new_curve.append(p1)
                new_curve.append(p2)
            elif isinstance(curve, QuadraticBezier):
                p1, p2 = complex_to_pair(curve.end)
                p3, p4 = complex_to_pair(curve.control)
                new_curve.append(p3)
                new_curve.append(p4)
                new_curve.append(p1)
                new_curve.append(p2)
                new_curve.append(p1)
                new_curve.append(p2)
            else:
                print(f'unkhown curve = {curve}')
        new_paths.append(
            SvgPath(path_arr=np.array(list(map(lambda c: c / 128, new_curve))), width=width, height=height))
    return SvgPicture(new_paths, png_file_path)


def get_initial_svg(png_file_path) -> SvgPicture:
    start_time = time.time()
    svg_path = os.path.join(THISDIR, f"tmp.svg")
    png_path = os.path.join(THISDIR, png_file_path)
    Path(svg_path).write_text(trace(png_path), encoding="utf-8")
    svg_pic = preprocess_svg_paths(svg_path, png_path)
    os.remove(svg_path)
    if config.DEBUG:
        print('Algo vectorization time = ', abs(time.time() - start_time), 'sec')
    return svg_pic


# For test
# get_initial_svg(f"tmp.svg", os.path.join("data", "AgapeDesign.png")).save_as_svg("lolkek.svg")
