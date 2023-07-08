import drawsvg as draw
import numpy as np


class SvgPath:
    path_arr: np.array
    width: int
    height: int
    segments_count: int

    def __init__(self, width: int, height: int, path_arr: np.array):
        self.width = width
        self.height = height
        self.path_arr = path_arr
        self.segments_count = (len(path_arr) - 2) // 6

    def __copy__(self):
        return SvgPath(self.width, self.height, np.array(self.path_arr))

    def set_path_arr(self, path_arr: np.array):
        self.path_arr = path_arr
        n_points = path_arr.shape[0]
        self.segments_count = (n_points - 2) // 6

    def create_drawing_object(self) -> draw.Path:
        assert self.path_arr is not None and len(self.path_arr) != 0

        path = draw.Path(
            fill='black',
            stroke='black',
            stroke_width=3.0,
            stroke_opacity=1.0
        )

        # Init start point
        x = float(self.path_arr[0] * self.width)
        y = float(self.path_arr[1] * self.height)
        path.M(x, y)

        # Init segments by Bezier curve
        segments = np.split(self.path_arr[2:], len(self.path_arr) // 6, axis=0)
        for el in segments:
            c1x = float(el[0] * self.width)
            c1y = float(el[1] * self.height)
            c2x = float(el[2] * self.width)
            c2y = float(el[3] * self.height)
            ex = float(el[4] * self.width)
            ey = float(el[5] * self.height)
            path.C(c1x, c1y, c2x, c2y, ex, ey)
        return path
