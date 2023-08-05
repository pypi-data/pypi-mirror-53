from collections import defaultdict
from typing import List

import numpy as np

from blackopt.abc import Problem, Solution
from blackopt.abc.solver import Solver



class GeneticAlgorithm(Solver):
    name = "GA"

    def __init__(
        self,
        problem: Problem,
        solution_cls,
        popsize: int,
        mutation_rate: float,
        elite_size: int,
    ):

        assert 0 < mutation_rate <= 1
        assert popsize > 1
        assert popsize > elite_size
        assert isinstance(elite_size, int)

        self.mutation_rate = mutation_rate
        self.popsize = popsize
        self.elite_size = elite_size

        super().__init__(problem, solution_cls)

        self.population: List[Solution] = [solution_cls.random_solution() for _ in range(popsize)]
        self.generation = 1
        self.avg = None
        self._rank()

    def solve(self, n_evaluations):

        while self.problem.eval_count < n_evaluations:

            next_generation = self.population[: self.elite_size]
            next_generation += self._breed(self.popsize - self.elite_size)
            self.population = next_generation

            self._rank()
            self.record()
            self.generation += 1
            print(self.generation)

        print(f"{self} is Done in {self.generation} generations")

    def _rank(self):
        self.population = sorted(self.population, key=lambda x: x.score, reverse=True)
        self.best_solution: Solution = max(self.population, key=lambda x: x.score)

    def record(self):
        super().record()
        aggr = defaultdict(list)
        for p in self.population:
            ms = p.metrics()
            for k, v in ms.items():
                aggr[k].append(v)
        for k, lst in aggr.items():
            self.record_metric(
                f"average_{k}",
                sum(lst) / self.popsize,
            )

    def _select_parents(self, n: int, smoothen_chances: float) -> List[Solution]:
        indexes = np.arange(0, len(self.population), dtype=np.int)
        chances = np.arange(
            len(self.population), 0, -1, dtype=np.int
        ) + smoothen_chances / (1 - smoothen_chances + 1e-9)
        chances = chances / sum(chances)
        parent_indexes = np.random.choice(indexes, n, True, chances)
        parents = np.array(self.population)[parent_indexes]

        return parents

    def _breed(self, n: int, smoothen_chances=0) -> List[Solution]:

        parents = self._select_parents(n, smoothen_chances)
        children: List[Solution] = []

        for i in range(n):
            parent_1 = parents[i]
            parent_2 = parents[len(parents) - i - 1]
            children += parent_1.crossover(parent_2)

        children = [child.mutate(self.mutation_rate) for child in children]

        return children

    def __str__(self):
        return (
            f"{self.name} with mut_rate - {self.mutation_rate} & "
            f"pop_size - {self.popsize} & "
            f"elite - {self.elite_size}"
        )
