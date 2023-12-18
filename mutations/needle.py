from dto.svg_picture import SvgPicture
from mutations.base import Mutation
import random

from mutations.needle_type.base import Type


class Needle(Mutation):
    type: Type

    def __init__(self, probability: float, needle_type: Type):
        super(Needle, self).__init__(probability)
        self.type = needle_type

    def __str__(self):
        return f'{__class__.__name__} (probability = {self.probability}, type = {self.type})'

    def __mutate__(self, picture: SvgPicture, gen_number: int) -> bool:
        random_path = picture.paths[random.randint(0, len(picture.paths) - 1)]
        random_segment = random_path.path_arr[random.randint(0, len(random_path.path_arr) - 1)]
        random_index = random.randint(0, random_segment.coordinates_count() - 1)
        random_coordinate_value = random_segment.get_value_by_index(random_index)
        sign = 1
        if random.random() < 0.5:
            sign = -1
        new_value = (random_coordinate_value + sign * self.type.get_ration(gen_number)) % 1
        if new_value != random_coordinate_value:
            random_segment.set_value_by_index(random_index, new_value)
            return True
        return False
