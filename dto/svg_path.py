import drawsvg as draw
import numpy as np
from typing import List

from dto.svg_segment import Segment, M, C
from utils.image import get_area


class SvgPath:
    path_arr: List[Segment]
    colors: List[np.array]
    width: int
    height: int
    segments_count: int

    def __init__(self, width: int, height: int, path_arr: List[Segment], colors: List[np.array] = []):
        self.width = width
        self.height = height
        self.path_arr = path_arr
        self.segments_count = len(path_arr)
        self.colors = colors

    def __copy__(self):
        path_arr = []
        colors = []
        for segment in self.path_arr:
            path_arr.append(segment.__copy__())
        for color in self.colors:
            colors.append(np.array(color))
        return SvgPath(self.width, self.height, path_arr, colors)

    def set_path_arr(self, path_arr: np.array):
        self.path_arr = path_arr
        self.segments_count = len(path_arr)

    def add_color(self, color: List[np.array]):
        for c in color:
            self.colors.append(c)

    def get_avg_colors(self) -> np.array:
        ans = []
        a = []
        colors_count = len(self.colors[0])
        for color in self.colors:
            color_arr = []
            for c in color:
                color_arr.append(c)
            ans.append(color_arr)
        ans = np.array(ans)
        for i in range(colors_count):
            a.append(sum(ans[:, i]) / len(ans))
        return np.array(a)

    @staticmethod
    def to_color(color: np.array) -> str:
        return f'rgb({color[0]},{color[1]},{color[2]})'

    def create_drawing_object(self) -> draw.Path:
        assert self.path_arr is not None and len(self.path_arr) != 0

        if len(self.colors) == 1:
            c = self.to_color(self.colors[0])
        else:
            area = get_area(self.path_arr, self.width, self.height)
            size = len(self.colors) - 1
            y = int((area.y1 - area.y0) / 2)
            c = draw.LinearGradient(area.x0, y, area.x1, y)
            for i, color in enumerate(self.colors):
                c.add_stop(i / size, self.to_color(color), 1)

        path = draw.Path(
            fill=c,
            stroke=c,
            stroke_width=1.0,
            stroke_opacity=1.0
        )

        for segment in self.path_arr:
            if isinstance(segment, M):
                path.M(segment.x, segment.y)
            elif isinstance(segment, C):
                c1x = segment.x
                c1y = segment.y
                c2x = segment.x1
                c2y = segment.y1
                ex = segment.x2
                ey = segment.y2
                path.C(c1x, c1y, c2x, c2y, ex, ey)

        return path
