import random

from dto.svg_picture import SvgPicture
from mutations.base import Mutation


class DropSegment(Mutation):

    def __init__(self, probability):
        super(DropSegment, self).__init__(probability)

    def __mutate__(self, picture: SvgPicture, gen_number: int) -> SvgPicture:
        random_path = picture.paths[random.randint(0, len(picture.paths) - 1)]
        random_segment_index = random.randint(0, len(random_path.path_arr) - 1)
        if len(random_path.path_arr) > 1:
            del random_path.path_arr[random_segment_index]
        return picture
