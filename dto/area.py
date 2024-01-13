class Area:
    x0: int
    y0: int
    x1: int
    y1: int

    def __init__(self, x0: int, y0: int, x1: int, y1: int):
        assert x0 <= x1 and y0 <= y1
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

    def get_area(self) -> int:
        return (self.x1 - self.x0) * (self.y1 - self.y0)

    def __str__(self):
        return f'Area(x0 = {self.x0}, y0 = {self.y0}, x1 = {self.x1}, y1 = {self.y1})'
