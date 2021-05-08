
class Row:
    def __init__(self, y: int, x: int, x_end: int, height: int):
        self.y = y
        self.height = height
        self.y_end = y + height
        self.x_end = x + x_end
        self.x = x
