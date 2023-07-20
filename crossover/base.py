import random
from typing import List

from dto.svg_picture import SvgPicture


class Crossover:

    def __init__(self):
        pass

    def crossover(self, population: List[SvgPicture]) -> List[SvgPicture]:
        assert len(population) > 0
        first, second = self.__choose_individuals__(population)
        self.__crossover__(first, second)
        return population

    def __choose_individuals__(self, population: List[SvgPicture]) -> (SvgPicture, SvgPicture):
        first = population[random.randint(0, len(population) - 1)]
        second = population[random.randint(0, len(population) - 1)]
        return first, second

    def __crossover__(self, first: SvgPicture, second: SvgPicture):
        pass
