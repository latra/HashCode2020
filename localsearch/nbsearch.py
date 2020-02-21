from random import random

from .interpretation import Interpretation
import math


class Solver:

    def __init__(self, problem: Interpretation):
        self.problem = problem
        self.best_sol = None
        self.best_cost = math.inf

    def solve(self, max_tries: int = 100, max_restarts: int = 30, rnd_walk: float = 0.1, file: str = '') -> Interpretation:
        curr_sol = self.problem.get_random_interpretation()
        self.best_sol = curr_sol
        self.best_cost = curr_sol.cost()
        for i in range(max_restarts):
            for mt in range(max_tries):
                if random() < rnd_walk:
                    curr_sol = curr_sol.get_random_walk()
                else:
                    curr_sol = curr_sol.get_best_neighbor()

                if self.best_cost > curr_sol.cost():
                    self.best_sol = curr_sol.copy()
                    self.best_cost = curr_sol.cost()
                    file_out = open(file, "w")
                    self.best_sol.print(file_out)
                    file_out.close()
                    if self.best_cost == 0:
                        return self.best_sol
            file_out = open(file, "w")
            self.best_sol.print(file_out)
            file_out.close()
        return self.best_sol


def main(model: Interpretation) -> None:
    best_sol = Solver(model).solve()
    print(best_sol.cost())
