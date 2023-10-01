from mutations.needle_type.base import Type


class ConstantType(Type):
    ratio: float

    def __init__(self, ratio):
        super().__init__()
        assert 0 <= ratio <= 1
        self.ratio = ratio

    def __str__(self):
        return f'ConstantType(ratio = {self.ratio})'

    def get_ration(self, gen_number: int):
        return self.ratio
