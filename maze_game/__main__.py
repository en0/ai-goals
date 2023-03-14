# Trying to solve a simple maze -> https://www.mathsisfun.com/games/mazes.html

import cv2
import numpy as np
from bs import ScreenGrabber, KeySender, ecodes as e
from bs.typing import Rect
from time import sleep
from typing import List, Optional, NamedTuple, Iterable, Tuple
from collections import deque


VIEWPORT: Rect = (553, 391, 1978, 1132)
TILESIZE = 57


class Vector2(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Vector2") -> "Vector2":
        x, y = other
        return Vector2(self.x + x, self.y + y)

    def __mul__(self, val: int) -> "Vector2":
        return Vector2(self.x * val, self.y * val)


class MazeMap:

    def __init__(self, grid: List[List[int]]):
        self._grid = grid

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
        except KeyError:
            return False

    def try_move(self, loc: Vector2, vector: Vector2) -> Vector2:
        """Try to move a direction.

        If successfull, returns new location. Else, returns None.
        """
        if self._is_walkable(loc + vector) and self._is_walkable(loc + vector * 2):
            return loc + vector * 2


class MazeAI:

    MOVE_DIRS = {
        e.KEY_UP: Vector2(0, -1),
        e.KEY_DOWN: Vector2(0, 1),
        e.KEY_LEFT: Vector2(-1, 0),
        e.KEY_RIGHT: Vector2(1, 0),
    }

    def __init__(self, keys: KeySender, screen: ScreenGrabber):
        self._keys = keys
        self._screen = screen
        self._maze: Optional[MazeMap] = None
        self._target: Optional[Vector2] = None
        self._loc: Optional[Vector2] = None

    def load_map(self):
        img = self._screen.grab_gray()
        th, tw = [x//TILESIZE for x in img.shape]
        img = cv2.resize(img, (tw, th), 0, 0, interpolation=cv2.INTER_NEAREST_EXACT)
        grid = [[1 if c == 189 else 0 for c in row] for row in img]
        self._maze = MazeMap(grid)
        self._loc = Vector2(1, 1)
        self._target = Vector2(tw-2, th-2)

    def find_moves_at(self, loc: Vector2) -> Iterable[Tuple[int, Vector2]]:
        """Finds the valid moves from the given location.

        Returns an iterator of tuples. Each tuple contains a valid direction and
        the new location if the given direction is applied
        """
        for direction, vector in self.MOVE_DIRS.items():
            new_loc = self._maze.try_move(loc, vector)
            if new_loc:
                yield direction, new_loc

    def find_with_bfs(self):
        stack = deque([(self._loc, [])])
        visited = {self._loc}
        while stack:
            loc, path = stack.popleft()
            if loc == self._target:
                return path
            for direction, next_loc in self.find_moves_at(loc):
                if next_loc not in visited:
                    visited.add(next_loc)
                    npath = path + [direction]
                    stack.append((next_loc, npath))

    def print_info(self, path: List[int] = None):
        print(self._maze)
        if path:
            print(", ".join([{
                e.KEY_UP: "UP",
                e.KEY_DOWN: "DOWN",
                e.KEY_LEFT: "LEFT",
                e.KEY_RIGHT: "RIGHT",
            }[p] for p in path]))
            print(f"Solved in {len(path)} moves.")

    def run(self):
        self.load_map()
        path = self.find_with_bfs()
        self.print_info(path)
        self._keys.send_many(path)


def main():
    wait = 3
    with ScreenGrabber(VIEWPORT) as screen:
        with KeySender() as keys:
            ai = MazeAI(keys, screen)
            print(f"You got {wait} second(s) to focus the screen...")
            sleep(wait)
            ai.run()


if __name__ == "__main__":
    main()

