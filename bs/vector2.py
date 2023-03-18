from typing import NamedTuple


class Vector2(NamedTuple):

    x: int
    y: int

    def __add__(self, other: "Vector2") -> "Vector2":
        x, y = other
        return Vector2(self.x + x, self.y + y)

    def __mul__(self, val: int) -> "Vector2":
        return Vector2(self.x * val, self.y * val)

