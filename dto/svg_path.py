import drawsvg as draw
import numpy as np
from typing import List

from dto.area import Area
from dto.svg_segment import Segment, M, C


class SvgPath:
    path_arr: List[Segment]
    color: np.array
    gradient_color: draw.LinearGradient
    width: int
    height: int
    segments_count: int

    def __init__(self, width: int, height: int, path_arr: List[Segment], color: np.array,
                 gradient_color: draw.LinearGradient = None):
        self.width = width
        self.height = height
        self.path_arr = path_arr
        self.color = color
        self.segments_count = len(path_arr)
        self.gradient_color = gradient_color

    def __copy__(self):
        path_arr = []
        for segment in self.path_arr:
            path_arr.append(segment.__copy__())
        return SvgPath(self.width, self.height, path_arr, np.array(self.color), self.gradient_color)

    def set_path_arr(self, path_arr: np.array):
        self.path_arr = path_arr
        self.segments_count = len(path_arr)

    def set_gradient_color(self, color1: np.array, color2: np.array, area: Area):
        y = int((area.y1 - area.y0) / 2)
        self.gradient_color = draw.LinearGradient(area.x0, y, area.x1, y)
        self.gradient_color.add_stop(0, self.to_color(color1), 1)
        self.gradient_color.add_stop(1, self.to_color(color2), 0)

    @staticmethod
    def to_color(color: np.array) -> str:
        return f'rgb({color[0]},{color[1]},{color[2]})'

    def create_drawing_object(self) -> draw.Path:
        assert self.path_arr is not None and len(self.path_arr) != 0

        if self.gradient_color is None:
            c = self.to_color(self.color)
        else:
            c = self.gradient_color

        path = draw.Path(
            fill=c,
            stroke=c,
            stroke_width=1.0,
            stroke_opacity=1.0
        )

        for segment in self.path_arr:
            if isinstance(segment, M):
                path.M(segment.x * self.width, segment.y * self.height)
            elif isinstance(segment, C):
                c1x = float(segment.x * self.width)
                c1y = float(segment.y * self.height)
                c2x = float(segment.x1 * self.width)
                c2y = float(segment.y1 * self.height)
                ex = float(segment.x2 * self.width)
                ey = float(segment.y2 * self.height)
                path.C(c1x, c1y, c2x, c2y, ex, ey)

        return path
