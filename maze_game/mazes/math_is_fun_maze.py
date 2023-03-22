from bs import Vector2
from typing import List
from ..typing import Maze, MazeFactory, MoveEnum


MOVE_TO_VECTOR = {
    MoveEnum.UP: Vector2(0, -1),
    MoveEnum.DOWN: Vector2(0, 1),
    MoveEnum.LEFT: Vector2(-1, 0),
    MoveEnum.RIGHT: Vector2(1, 0),
}


class MathIsFunMaze(Maze):
    """Represents a maze loaded from MathIsFun.com.

    The mazes on MathIsFun.com moves 2 grid units at a time.
    For example, if you are currently at the location (1, 1) and wanted to move one
    step to the right, your location after the move would be (3, 1).

    Ref: https://www.mathsisfun.com/measure/mazes.html
    """

    def __init__(self, grid: List[List[int]], start: Vector2, target: Vector2):
        self._grid = grid
        self._start = start
        self._target = target

    def __repr__(self):
        ret = []
        for y, row in enumerate(self._grid):
            out = []
            for x, c in enumerate(row):
                if c == 1:
                    out.append('X')
                else:
                    out.append(' ')
            ret.append(" ".join(out))
        return "\n".join(ret)

    def _is_walkable(self, loc: Vector2) -> bool:
        try:
            x, y = loc
            return self._grid[y][x] == 0
        except IndexError:
            return False

    def try_move(self, loc: Vector2, move: MoveEnum) -> Vector2:
        vector = MOVE_TO_VECTOR[move]
        if self._is_walkable(loc + vector) and self._is_walkable(loc + vector * 2):
            return loc + vector * 2

    @property
    def start(self):
        return self._start

    @property
    def target(self):
        return self._target

    @property
    def height(self):
        return len(self._grid)

    @property
    def width(self):
        return len(self._grid[0])


class MathIsFunMazeFactory(MazeFactory):
    def create(self, grid, start, target):
        return MathIsFunMaze(grid, start, target)

