import random

import config
from dto.svg_picture import SvgPicture


class Mutation:
    probability: float

    def __init__(self, probability):
        assert 0 <= probability <= 1
        self.probability = probability

    def mutate(self, picture: SvgPicture, gen_number: int) -> SvgPicture:
        if len(picture.paths) == 0:
            if config.DEBUG:
                print("No paths for needle mutation")
            return picture

        if random.random() < self.probability:
            self.__mutate__(picture, gen_number)
        return picture

    def __mutate__(self, picture: SvgPicture, gen_number: int) -> SvgPicture:
        return picture
