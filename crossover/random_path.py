import random

from crossover.base import Crossover
from dto.svg_picture import SvgPicture


class RandomPath(Crossover):

    def __init__(self):
        super().__init__()

    def __crossover__(self, first: SvgPicture, second: SvgPicture):
        assert len(first.paths) > 0 and len(second.paths) > 0
        first_random_index = random.randint(0, len(first.paths) - 1)
        second_random_index = random.randint(0, len(second.paths) - 1)

        first_path = first.paths[first_random_index]
        second_path = first.paths[second_random_index]

        first.paths.append(second_path.__copy__())
        second.paths.append(first_path.__copy__())

        del first.paths[first_random_index]
        del second.paths[second_random_index]
