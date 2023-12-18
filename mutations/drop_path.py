import random

from dto.svg_picture import SvgPicture
from mutations.base import Mutation
from utils.image import get_area


class DropPath(Mutation):
    max_drop_area_percent: float

    def __init__(self, probability, max_drop_area_percent=1):
        super(DropPath, self).__init__(probability)
        self.max_drop_area_percent = max_drop_area_percent

    def __str__(self):
        return f'{__class__.__name__} (probability = {self.probability}, max_drop_area_percent = {self.max_drop_area_percent})'

    def __mutate__(self, picture: SvgPicture, gen_number: int) -> bool:
        random_path_index = random.randint(0, len(picture.paths) - 1)
        random_path_area = get_area(picture.paths[random_path_index].path_arr, picture.width, picture.height).get_area()
        has_suitable_size_for_drop = random_path_area / (picture.width * picture.height) <= self.max_drop_area_percent
        if has_suitable_size_for_drop:
            picture.del_path(random_path_index)
            return True
        return False
