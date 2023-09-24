import random
import numpy as np

from dto.svg_picture import SvgPicture
from mutations.base import Mutation
from utils.image import get_area


class ConcatPath(Mutation):
    diff_color: int = 256 + 256 + 256

    def __init__(self, probability):
        super(ConcatPath, self).__init__(probability)

    def __str__(self):
        return f'{__class__.__name__} (probability = {self.probability}, diff_color = {self.diff_color})'

    def __mutate__(self, picture: SvgPicture, gen_number: int) -> SvgPicture:
        random_path_index1 = random.randint(0, len(picture.paths) - 1)
        random_path_index2 = random.randint(0, len(picture.paths) - 1)
        path1 = picture.paths[random_path_index1]
        path2 = picture.paths[random_path_index2]
        diff_color = abs(np.sum(np.subtract(path1.color, path2.color)))
        if len(picture.paths) > 1 and diff_color <= self.diff_color and random_path_index1 != random_path_index2 \
                and path1.gradient_color is None and path2.gradient_color is None:
            new_path = path1.path_arr.copy()
            for segment in path2.path_arr:
                new_path.append(segment)
            path1.set_path_arr(new_path)
            area = get_area(path1, picture.width, picture.height)
            path1.set_gradient_color(path1.color, path2.color, area)
            del path2
        return picture
