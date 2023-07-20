import config
from dto.svg_picture import SvgPicture
from mutations.base import Mutation
import random


class Needle(Mutation):

    def __init__(self, probability):
        super(Needle, self).__init__(probability)

    def __mutate__(self, picture: SvgPicture, gen_number: int) -> SvgPicture:
        random_path = picture.paths[random.randint(0, len(picture.paths) - 1)]
        random_segment = random_path.path_arr[random.randint(0, len(random_path.path_arr) - 1)]
        random_index = random.randint(0, random_segment.coordinates_count() - 1)
        random_coordinate = random_segment.get_value_by_index(random_index)
        sign = 1
        if random.random() < 0.5:
            sign = -1
        new_value = (random_coordinate + sign * (0.1 - (0.1 / config.STEP_EVOL) * gen_number)) % 1
        random_segment.set_value_by_index(random_index, new_value)
        return picture
