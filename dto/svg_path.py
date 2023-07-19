import drawsvg as draw
import numpy as np
from typing import List

from dto.svg_segment import Segment, M, C


class SvgPath:
    path_arr: List[Segment]
    color: np.array
    width: int
    height: int
    segments_count: int

    def __init__(self, width: int, height: int, path_arr: List[Segment], color: np.array):
        self.width = width
        self.height = height
        self.path_arr = path_arr
        self.color = color
        self.segments_count = len(path_arr)

    def __copy__(self):
        path_arr = []
        for segment in self.path_arr:
            path_arr.append(segment.__copy__())
        return SvgPath(self.width, self.height, path_arr, np.array(self.color))

    def set_path_arr(self, path_arr: np.array):
        self.path_arr = path_arr
        self.segments_count = len(path_arr)

    def create_drawing_object(self) -> draw.Path:
        assert self.path_arr is not None and len(self.path_arr) != 0

        path = draw.Path(
            fill=self.color,
            stroke=self.color,
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
