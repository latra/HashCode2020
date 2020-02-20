from __future__ import annotations

import random
import sys
from typing import List, Dict

from .interpretation import Interpretation


class Book:

    def __init__(self, score: int):
        self.score = score
        self.order = -1

    def set_order(self, num):
        self.order = num


class Library:

    def __init__(self, books: List[Book], signup: int, capacity: int, ):
        self.books: List[Book] = books
        self.signup: int = signup
        self.capacity: int = capacity


class Lib(Interpretation):

    def __init__(self, libraries: List[Library], deadline: int, best_score: int, books, max_neighbors):
        super().__init__()
        self.libraries: List[Library] = libraries
        self.books: Dict[int, Book] = books
        self.inter: Dict[int, (Library, int)] = {}
        self.deadline = deadline
        self.best_score = best_score
        self.get_random_interpretation()
        self.max_neigh = max_neighbors

    def cost(self) -> int:
        sum_cost = 0
        for _, instance in self.books.items():
            sum_cost += instance.score
        return self.best_score - sum_cost

    def get_random_interpretation(self) -> Interpretation:
        for day in range(self.deadline):
            lib_id = random.randint(0, len(self.libraries) - 1)
            self.inter[lib_id] = self.libraries[lib_id], day
            current_library = self.libraries[lib_id]
            acc_day, bag = 0, 0
            for i, book in enumerate(self.libraries[lib_id].books):
                if current_library.capacity == bag:
                    bag = 0
                    acc_day += 1
                self.books[i].set_order(day + current_library.signup + acc_day)
                bag += 1
        return self

    def copy(self) -> Lib:
        c = Lib(self.libraries, self.deadline, self.best_score, self.books, self.max_neigh)
        return c

    def print(self) -> None:
        pass

    def _get_list_neighbors(self) -> List[Interpretation]:
        res = []
        for i in range(self.max_neigh):
            neigh: Lib = self.copy()
            lib_id1 = random.randint(0, len(self.libraries) - 1)
            lib_id2 = random.randint(0, len(self.libraries) - 1)
            tmp = neigh.inter[lib_id1]
            neigh.inter[lib_id1] = lib_id2
            neigh.inter[lib_id2] = tmp
            res.append(neigh)
        return res

    def get_best_neighbor(self) -> Interpretation:
        best_cost = self.best_score
        best_sol = None
        for neigh in self._get_list_neighbors():
            if neigh.cost() < best_cost:
                best_cost = neigh.cost()
                best_sol = neigh
        return best_sol

    def get_random_walk(self) -> List[Interpretation]:
        nbs = self._get_list_neighbors()
        return nbs[random.randint(0, len(nbs) - 1)]


def main():
    is_book_signed = {}
    for _id in range(num_books):
        is_book_signed[_id] = Book()
    sum() // scores
    inter = Lib()


if __name__ == '__main__':
    main(sys.argv[0])
