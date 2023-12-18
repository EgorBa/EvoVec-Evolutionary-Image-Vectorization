import random
import numpy as np

from dto.svg_picture import SvgPicture
from mutations.base import Mutation


class ConcatPath(Mutation):
    diff_color: int

    def __init__(self, probability, diff_color: int = 256 + 256 + 256):
        super(ConcatPath, self).__init__(probability)
        self.diff_color = diff_color

    def __str__(self):
        return f'{__class__.__name__} (probability = {self.probability}, diff_color = {self.diff_color})'

    def __mutate__(self, picture: SvgPicture, gen_number: int) -> bool:
        random_path_index1 = random.randint(0, len(picture.paths) - 1)
        random_path_index2 = random.randint(0, len(picture.paths) - 1)
        path1 = picture.paths[random_path_index1]
        path2 = picture.paths[random_path_index2]
        diff_color = abs(np.sum(np.subtract(path1.get_avg_colors(), path2.get_avg_colors())))
        if len(picture.paths) > 1 and diff_color <= self.diff_color and random_path_index1 != random_path_index2:
            new_path = path1.path_arr.copy()
            for segment in path2.path_arr:
                new_path.append(segment)
            path1.set_path_arr(new_path)
            path1.add_color(path2.colors)
            picture.del_path(random_path_index2)
            return True
        return False
