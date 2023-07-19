class Segment:

    def __init__(self):
        pass

    def __copy__(self):
        pass

    def __str__(self):
        pass

    def coordinates_count(self) -> int:
        return 0

    def get_value_by_index(self, index: int) -> float:
        return 0.0

    def set_value_by_index(self, index: int, value: float):
        pass


class M(Segment):
    x: float
    y: float

    def __init__(self, x: float, y: float):
        super().__init__()
        self.x = x
        self.y = y

    def __copy__(self):
        super().__copy__()
        return M(self.x, self.y)

    def __str__(self):
        return f'M(x = {self.x}, y = {self.y})'

    def coordinates_count(self) -> int:
        return 2

    def get_value_by_index(self, index: int) -> float:
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        return super().get_value_by_index(index)

    def set_value_by_index(self, index: int, value: float):
        if index == 0:
            self.x = value
        if index == 1:
            self.y = value


class C(Segment):
    x: float
    y: float
    x1: float
    y1: float
    x2: float
    y2: float

    def __init__(self, x: float, y: float, x1: float, y1: float, x2: float, y2: float):
        super().__init__()
        self.x = x
        self.y = y
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __copy__(self):
        super().__copy__()
        return C(self.x, self.y, self.x1, self.y1, self.x2, self.y2)

    def __str__(self):
        return f'C(x = {self.x}, y = {self.y}, x1 = {self.x1}, y1 = {self.y1}, x2 = {self.x2}, y2 = {self.y2})'

    def coordinates_count(self) -> int:
        return 6

    def get_value_by_index(self, index: int) -> float:
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        if index == 2:
            return self.x1
        if index == 3:
            return self.y1
        if index == 4:
            return self.x2
        if index == 5:
            return self.y2
        return super().get_value_by_index(index)

    def set_value_by_index(self, index: int, value: float):
        if index == 0:
            self.x = value
        if index == 1:
            self.y = value
        if index == 2:
            self.x1 = value
        if index == 3:
            self.y1 = value
        if index == 4:
            self.x2 = value
        if index == 5:
            self.y2 = value
