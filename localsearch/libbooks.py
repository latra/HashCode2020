from __future__ import annotations

import random
import sys
from typing import List, Dict, Tuple, TextIO, IO
from localsearch.interpretation import Interpretation


class Book:

    def __init__(self, book_id: int, score: int):
        self.book_id = book_id
        self.score = score
        self.order = -1

    def set_order(self, num):
        self.order = num


class Library:

    def __init__(self, lib_id: int, books: List[Book], signup: int, capacity: int, total_books: int):
        self.lib_id = lib_id
        self.books: List[Book] = books
        self.signup: int = signup
        self.capacity: int = capacity
        self.total_books: int = total_books
        self.picked_books: List[Book] = []


class Lib(Interpretation):

    def __init__(self, libraries: List[Library], deadline: int, best_score: int, books: Dict[int, Book], max_neighbors):
        super().__init__()
        self.libraries: List[Library] = libraries
        self.books: Dict[int, Book] = books
        self.inter: Dict[int, Tuple[Library, int]] = {}
        self.libs_from_books: Dict[int, List[int]] = {}
        self.picked_books: Dict[int, Book] = {}
        self.deadline = deadline
        self.best_score = best_score
        self.max_neigh = max_neighbors
        self.picked_libs = 0

    def score(self):
        sum_cost = 0
        for _, instance in self.picked_books.items():
            sum_cost += instance.score
        return sum_cost

    def cost(self) -> int:
        return self.best_score - self.score()

    def get_random_interpretation(self) -> Interpretation:
        for day in range(self.deadline):
            lib_id = random.randint(0, len(self.libraries) - 1)
            while lib_id in self.inter:
                lib_id = random.randint(0, len(self.libraries) - 1)
            self.inter[lib_id] = self.libraries[lib_id], day
            current_library = self.libraries[lib_id]
            acc_day, bag = 0, 0
            checked_books = []
            for i, book in enumerate(self.libraries[lib_id].books):
                if book.book_id not in self.picked_books:
                    if current_library.capacity == bag:
                        bag = 0
                        acc_day += 1
                    if acc_day + day == self.deadline:
                        break
                    self.books[i].set_order(day + current_library.signup + acc_day)
                    bag += 1
                    checked_books.append(i)
                    self.picked_books[book.book_id] = book
                    self.libraries[lib_id].picked_books.append(book)
            self.libs_from_books[lib_id] = checked_books
            self.picked_libs += 1
            if len(self.inter) == len(self.libraries):
                return self
        return self

    def copy(self) -> Lib:
        c = Lib(self.libraries, self.deadline, self.best_score, self.books, self.max_neigh)
        c.inter = self.inter
        c.picked_libs = self.picked_libs
        c.picked_books = self.picked_books
        return c

    def print(self, file_out: TextIO) -> None:
        sys.stderr.write("============\n")
        file_out.write(str(self.picked_libs) + '\n')
        libraries = self.get_correct_order()
        for dia, lib in libraries.items():
            lib_id, library = lib
            if len(library.picked_books) != 0:
                file_out.write(str(lib_id) + " " + str(len(library.picked_books)) + '\n')
                file_out.write(" ".join(map(str, [book.book_id for book in library.picked_books])) + '\n')
        sys.stderr.write("S'ha trobat solució\n")
        sys.stderr.write("COST: ==> " + str(self.score()) + '\n')
        sys.stderr.write("============\n")

    def _get_list_neighbors(self) -> List[Interpretation]:
        res = []
        for i in range(self.max_neigh):
            neigh: Lib = self.copy()
            random.random(self.picked_libs)
            lib_id1 = random.randint(0, len(self.libraries) - 1)
            lib_id2 = random.randint(0, len(self.libraries) - 1)
            tmp1 = self.inter[lib_id1]
            tmp2 = self.inter[lib_id2]
            neigh.inter[lib_id1] = tmp1[0], tmp2[1]
            neigh.inter[lib_id2] = tmp2[0], tmp1[1]
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

    def get_correct_order(self) -> Dict[int, Tuple[int, Library]]:
        res: Dict[int, (int, Library)] = {}
        for lib_id, tup in self.inter.items():
            lib, dia = tup
            res[dia] = lib_id, lib
        return res


def main(data_id: int, file_p: str):
    from localsearch.nbsearch import Solver
    datasetURLs = [
        "https://hashcodejudge.withgoogle.com/download/blob/AMIfv96z2wILTmc0q35abZk6s8nklnGSRLd0IKa2jein6k8THmQLBlLCj144Yi8ih04jwPxn0ubGUsOWVha5w7UOMt0oLsSYtafv_oqVogstm7ve0br1JiNJ8IRE55Fgq2i6zRGNCTwjOU0gJJuRvevzTcP2Cq8_l5f9UcHJbfOfB0sq4evSBNx8gBMXZzNLUfpKppv848Z4XQ2Eh6e6qwfZO2QXbGnjnxuWNBDXYzdiMYd6CHI6qIHmY9K8pr81n4IaR9nF0_uESJ87ckK0lkNSX1c5VpCCfDxmVCM6DyYr2uWzEv15FKB0z0grxBdIy7Ek0M_L5GdR",
        "https://hashcodejudge.withgoogle.com/download/blob/AMIfv94kPv9bNHpmvuYRrlBfNhpxJTP3rqdEnAvWKPOmvlXWKTh4B3r-zEpdPVLqCmRr2a2U6NlmOseGUaKgA2MBL1R0smk2Yp5T4BBM5ksZ1ORlFESooGzvy7FMkB8QdideiU7DRpYIMBZ9n6iPDrJFYwWcvCa0lHkvFJkNVDhewrTmeunr24d_LaIVyKZ0DUiD9LSRFQXdG7aHc_7mnNPsv9j0l4LZCpFgdPDuA_i3Iowsi-dw7Jz9jiXhUO24DPm7iHoTqTB6hYGnkR-sUl1AJjFWa7q4xbe2EI3gh-ctcvdrIP92gE60ALO_-K57K6-esBJiYVqx",
        "https://hashcodejudge.withgoogle.com/download/blob/AMIfv95NC_WFM6Jsbq9RYjiBXGn1NaSHn6ZUu2NGyX_ez-9YgExaDbROx5QHPAb5UbBCOj4JXU25gZZN0a-q7x_CqqtG9DfLsewBlNb-bGTpBidu1rGh8UWRVB8P4z39RUaZYu3C7UuhE9WF4aUUmA1Xq847HKJDqJ22ksunXBGAnYI61yglZp_wOyzmdp0i_tRSmlO-Jj60bzgB084z3GUYfy00_Kih1c0f7g3iHIPr4FjlxY_4s4rZcJp29yrJHp_dDGZPGsK65tmtmK5c1kptuin39knpKc0tQ2hmJhV-YBNtvyVCvc-wVoM-0f4GsSCbUMnGmu-r",
        "https://hashcodejudge.withgoogle.com/download/blob/AMIfv94EswDoarsD_T8xfMl8Lx_Bb1V9ppyCMQuCsTXwowKBQ_JFwr9PzEVxgeAgwIeUbZU6R6sg2vrGKpBVKjpwfRfqJxFHOEobK82DVjKwLgi5jkGw3W3td09e18wF_xRXHtC2vewVhS0CyLoju7ykI9qLhZlaJI5ITzOSEKsPlT5sgkjCPFMK10ebbniYT4wKFAFGEMLkIolRCkgVAO0Fo2J20yNbrHbYkzZGbPS7Hq84DRX4rng0sT-HUXTYzZmRtzneJEg8-KD6vIJi4cCr8x4GgspQl_nZzCvnQ8If3PMDiFoqWF5JXW6ZjrpZWO9w6KTtvJAv",
        "https://hashcodejudge.withgoogle.com/download/blob/AMIfv94DTMLimuIhJSCxbRWjE9-zrgGFV3pPJJn6Gdt5z8qw4xGLbPyCSmfbkm7OXiWDTqVLV_KMGcYGDghaDnaAVLeooSukTi-ISm-NwZrbyYD_Mme7oF0i4BgDot0jbzE3aeBPa2jQSAjrGl3Rn7HAf1zmI875X5hPKxfOAie4JhY1ilZ259Ws5dm-16pZEVCON0qOqJyp1otWRLvkS1ik-E4viEB0ZAGANfwGEGCaFBFw6BP-5s-qQJwEFhcSkMOt_yoqo-Kh48eSl53aIy4wt9Wv5sgDt6dNgpg8i-ZZD9MJ8ZdNf-YShMvAhTf268TUaScyv3WIç",
        "https://hashcodejudge.withgoogle.com/download/blob/AMIfv97dgUsRkZX-sPN6ZjxVuupAVdZtpeLNfh2m1Y1brcUXLNq4SuwjqPA8Adl4FcNRewazJSiXfhQxjlgUNOnxlSF9hJxJdBzl2LIthcs2VBrD41rNUtd077k277McQLMFgwx1qPjvwnynXnUAZqE3F8XiTq9uOpAWSuMW1h8nbJwNCDcrH3-0ZPxW-3AGbozbJw6jWpCYuF2Gsq5Ato2ijJtI_hq9_7Oj37ddoFsYXOJnLO0toEK-hP4c9ItPQWm4SvrI3X2NPckkP15ImXsUhFXohgj-ZaudpG7he0X4oqpWoLAzJ3M0UyfMKHF5P9O1bLU-yi-8"
    ]
    from localsearch.searchdataset import Dataset
    d = Dataset(datasetURLs[data_id])
    total_score = sum([book.score for book in d.books])
    hash_books = {}
    for book in d.books:
        hash_books[book.book_id] = book
    lib = Lib(d.libraries, d.total_days, total_score, hash_books, 8)
    solver = Solver(lib)
    solver.solve(1000, 9000000, 0.1, file_p)


if __name__ == '__main__':
    main(int(sys.argv[0]))
