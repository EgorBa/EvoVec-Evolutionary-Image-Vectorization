import random

from dto.svg_picture import SvgPicture
from mutations.base import Mutation


class DropPath(Mutation):

    def __init__(self, probability):
        super(DropPath, self).__init__(probability)

    def __mutate__(self, picture: SvgPicture, gen_number: int) -> SvgPicture:
        random_path_index = random.randint(0, len(picture.paths) - 1)
        if len(picture.paths) > 1:
            del picture.paths[random_path_index]
        return picture
