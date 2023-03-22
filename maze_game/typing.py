from abc import ABC, abstractmethod
from typing import List
from enum import IntEnum, auto
from bs import Vector2


class MoveEnum(IntEnum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class Maze(ABC):

    @abstractmethod
    def try_move(self, loc: Vector2, move: MoveEnum) -> Vector2:
        """Try to move a direction.

        Arguments:
            loc: A vector that identifies the location to move from.
            move: A MoveEnum describing the move to make.

        Returns:
            If successfull, a new location.
            Else, None.
        """
        ...

    @property
    @abstractmethod
    def height(self):
        ...

    @property
    @abstractmethod
    def width(self):
        ...

    @property
    @abstractmethod
    def start(self):
        ...

    @property
    @abstractmethod
    def target(self):
        ...


class MazeFactory(ABC):

    @abstractmethod
    def create(self, grid: List[List[int]], start: Vector2, target: Vector2) -> Maze:
        """Create a maze from the given arguments

        Arguments:
            grid: A 2d list describing the maze walkable areas.
            start: A vector describing the start position in the maze.
            target: A vector describing the end position in the maze.
        """
        ...


class MazeLoader(ABC):

    @abstractmethod
    def load(self) -> Maze:
        """Load a maze

        Returns:
            A maze.
        """
        ...


class Solver(ABC):

    @abstractmethod
    def solve(self, maze: Maze) -> List[MoveEnum]:
        """Solve a maze.

        Arguments:
            maze: The maze to solve.

        Returns:
            A list of MoveEnums.
        """
        ...

