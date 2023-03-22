from bs import ScreenGrabber, KeySender
from time import sleep
from typing import List

from .typing import MazeLoader, MoveEnum, Solver, Maze
from .loaders import EdgeDetectingMazeLoader
from .mazes import MathIsFunMazeFactory
from .key_sender_adapter import KeySenderAdapter
from .solvers import DFSSolver, GeneticSolver, SupervisedLearningSolver


class MazeAI:

    def __init__(self, sender: KeySenderAdapter, loader: MazeLoader, solver: Solver):
        self._sender = sender
        self._loader = loader
        self._solver = solver

    def _show(self, maze: Maze, path: List[MoveEnum] = None):
        print(maze)
        if path:
            print(", ".join(map(lambda a: str(a).split('.')[-1], path)))
            print(f"Solved in {len(path)} moves.")

    def run(self):
        maze = self._loader.load()
        path = self._solver.solve(maze)
        self._show(maze, path)
        self._sender.send_many(path)


def main():
    wait = 1
    solvers = [
        DFSSolver(),
        GeneticSolver(),
        SupervisedLearningSolver()
    ]
    with ScreenGrabber() as screen:
        with KeySender() as sender:
            ai = MazeAI(
                sender=KeySenderAdapter(sender),
                solver=solvers[2],
                loader=EdgeDetectingMazeLoader(
                    screen=screen,
                    factory=MathIsFunMazeFactory(),
                )
            )
            print(f"You got {wait} second(s) to focus the screen...")
            sleep(wait)
            ai.run()


if __name__ == "__main__":
    main()

