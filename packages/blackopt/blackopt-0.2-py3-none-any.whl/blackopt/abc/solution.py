from __future__ import annotations
import abc
from typing import TYPE_CHECKING, List, Dict, SupportsFloat

if TYPE_CHECKING:
    from blackopt.abc import Problem


class Solution(abc.ABC):
    problem: Problem = None
    _score: float = None

    @staticmethod
    @abc.abstractmethod
    def random_solution() -> Solution:
        raise NotImplementedError()

    @abc.abstractmethod
    def mutate(self, rate: float) -> Solution:
        raise NotImplementedError()

    @abc.abstractmethod
    def crossover(self, other: Solution) -> List[Solution]:
        raise NotImplementedError()

    @property
    def score(self):
        if self._score is None:
            self._score = self.problem.evaluate(self)
        return self._score

    def metrics(self) -> Dict[str, SupportsFloat]:
        return {"score": self.score}
