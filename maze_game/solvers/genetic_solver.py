from typing import List, Optional
from random import choices, randint, choice
from ..typing import Solver, Maze, MoveEnum


MOVES = list(MoveEnum)
Genome = List[MoveEnum]


class GeneticSolver(Solver):

    def __init__(self):
        self._population_size = 1000
        self._fitness_limit = int(self._population_size * 0.05)
        self._limit: Optional[int] = None
        self._maze: Optional[Maze] = None
        self._solution: Optional[Genome] = None
        self._top_score: int = 0

    def solve(self, maze: Maze) -> List[MoveEnum]:
        self._maze = maze
        self._limit = maze.height * maze.width
        _population = self._sort([choices(MOVES, k=self._limit) for _ in range(self._population_size)])
        while not self._solution:
            _population = self._repopulate(_population)
            _population = self._sort(_population)
            print(self._top_score, _population[0][:10])
        return self._trim_moves(self._solution)

    def _trim_moves(self, genome: Genome) -> Genome:
        new_loc = self._maze.start
        trimmed = []
        for move in genome:
            new_loc = self._maze.try_move(new_loc, move)
            trimmed.append(move)
            if new_loc == self._maze.target:
                return trimmed

    def _compute_fitness(self, genome: Genome) -> int:
        new_loc = self._maze.start
        visited = set([new_loc])
        score = 0
        for move in genome:
            new_loc = self._maze.try_move(new_loc, move)
            if new_loc == None:
                return score
            elif new_loc in visited:
                return score
            elif new_loc == self._maze.target:
                self._solution = genome
                return score
            else:
                score += 1
                visited.add(new_loc)
                self._top_score = max(self._top_score, score)

    def _sort(self, population: List[Genome]) -> List[Genome]:
        return sorted(population, key=self._compute_fitness, reverse=True)

    def _repopulate(self, population: List[Genome]) -> List[Genome]:
        parents = population[0:self._fitness_limit] + population[-self._fitness_limit:]
        new_population = []
        while len(new_population) < self._population_size:
            a, b = choices(parents, k=2)
            genome = self._crossover(a, b)
            genome = self._mutate(genome)
            new_population.append(genome)
        return new_population

    def _crossover(self, a: Genome, b: Genome) -> Genome:
        k = randint(0, len(a) - 1)
        return a[:k] + b[k:]

    def _mutate(self, a: Genome) -> Genome:
        b = a.copy()

        if randint(1, 2) == 1:
            while True:
                if randint(1, 3) != 3:
                    return b
                k = randint(0, len(b) - 1)
                b[k] = choice(MOVES)
        else:
            while True:
                if randint(1, 3) != 3:
                    return b
                k = randint(0, len(b) - 1)
                b = b[k:] + b[:k]
        return b



