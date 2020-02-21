import sys

from .interpretation import Interpretation
import math


class Solver:

    def __init__(self, problem: Interpretation):
        self.problem = problem
        self.best_sol = None
        self.best_cost = math.inf

    def solve(self, max_tries: int = 100000000000, file: str = '') -> Interpretation:
        for i in range(max_tries):
            curr_sol = self.problem.get_random_interpretation()
            if curr_sol.cost() < self.best_cost:
                self.best_sol = curr_sol.copy()
                self.best_cost = curr_sol.cost()
                file_out = open(file, "w")
                self.best_sol.print(file_out)
                file_out.close()
                if self.best_cost == 0:
                    return self.best_sol
        return self.best_sol


def main(model: Interpretation) -> None:
    best_sol = Solver(model).solve()
    print(best_sol.cost())
    best_sol.print()
