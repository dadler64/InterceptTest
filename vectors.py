import math

class Vec2D:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def add(self, x: float, y: float):
        return Vec2D(self.x + x, self.y + y)

    def subtract(self, x: float, y: float):
        return Vec2D(self.x - x, self.y - y)

    def length(self) -> float:
        length = math.sqrt(((self.x ** 2) + (self.y ** 2)))
        return float(length)

    def dot(self, x: float, y: float):
        return Vec2D(self.x * x, self.y * y)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"
