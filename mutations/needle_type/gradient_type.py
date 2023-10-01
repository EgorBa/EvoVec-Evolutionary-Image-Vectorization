import config
from mutations.needle_type.base import Type


class GradientType(Type):
    start_ratio: float
    end_ratio: float

    def __init__(self, start_ratio, end_ratio):
        super().__init__()
        assert 0 <= start_ratio <= 1 and 0 <= end_ratio <= 1
        self.start_ratio = start_ratio
        self.end_ratio = end_ratio

    def __str__(self):
        return f'GradientType(start_ratio = {self.start_ratio}, end_ratio = {self.end_ratio})'

    def get_ration(self, gen_number: int):
        p = config.STEP_EVOL / gen_number
        return self.start_ratio + p * (self.end_ratio - self.start_ratio)
