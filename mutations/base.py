import random

import config
from dto.svg_picture import SvgPicture


class Mutation:
    probability: float

    def __init__(self, probability):
        assert 0 <= probability <= 1
        self.probability = probability

    def __str__(self):
        return __class__.__name__

    def mutate(self, picture: SvgPicture, gen_number: int) -> SvgPicture:
        if len(picture.paths) == 0:
            if config.DEBUG:
                print("No paths for mutation")
            return picture

        if random.random() < self.probability:
            if self.__mutate__(picture, gen_number):
                picture.fitness = -1
        return picture

    def __mutate__(self, picture: SvgPicture, gen_number: int) -> bool:
        return False
