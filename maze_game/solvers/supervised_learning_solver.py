from typing import List, Optional
from random import choices, randint, choice
from ..typing import Solver, Maze, MoveEnum


MOVES = list(MoveEnum)


class SupervisedLearningSolver(Solver):

    def __init__(self):
        ...

    def solve(self, maze: Maze) -> List[MoveEnum]:
        return []

