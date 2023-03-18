from bs import Vector2
from typing import List, Iterable, Tuple
from collections import deque

from ..typing import MoveEnum, Solver, Maze


class DFSSolver(Solver):

    def _find_moves_at(self, maze: Maze, loc: Vector2) -> Iterable[Tuple[int, Vector2]]:
        """Finds the valid moves from the given location.

        Returns an iterator of tuples. Each tuple contains a valid MoveEnum and
        the new location if the given move is applied
        """
        for move in MoveEnum:
            new_loc = maze.try_move(loc, move)
            if new_loc:
                yield move, new_loc

    def solve(self, maze: Maze) -> List[MoveEnum]:
        """search for the best path using a breadth-first-search"""
        stack = deque([(maze.start, [])])
        visited = {maze.start}
        while stack:
            loc, path = stack.popleft()
            if loc == maze.target:
                return path
            for move, next_loc in self._find_moves_at(maze, loc):
                if next_loc not in visited:
                    visited.add(next_loc)
                    npath = path + [move]
                    stack.append((next_loc, npath))

