from __future__ import annotations

import random
import sys
from typing import List, TextIO, Dict, Optional
from functools import reduce

from localsearch.interpretation import Interpretation


class Book:

    def __init__(self, book_id: int, score: int):
        self.book_id: int = book_id
        self.score = score

    def __eq__(self, other: Book):
        return self.score == other.score

    def __lt__(self, other: Book):
        return self.score < other.score

    def __gt__(self, other: Book):
        return self.score > other.score

    def __le__(self, other: Book):
        return self.score <= other.score

    def __ge__(self, other: Book):
        return self.score >= other.score

    def __str__(self):
        return f"[%d: %d]" % (self.book_id, self.score)


class Library:

    def __init__(self, lib_id: int, total_books: Dict[int, Book], days_signup: int, capacity: int):
        self.lib_id: int = lib_id
        self.picked_books: List[Book] = []
        self.total_books: Dict[int, Book] = total_books
        self.signup: int = days_signup
        self.default_signup: int = days_signup
        self.capacity: int = capacity

    def add_book(self, book: Book) -> None:
        self.picked_books.append(book)

    def dec_signup(self) -> None:
        self.signup -= 1

    def sort_books(self) -> None:
        total_books = list(self.total_books.values())
        total_books.sort()
        total_books.reverse()
        self.total_books = dict([(book.book_id, book) for book in total_books])

    def __str__(self):
        books = " ".join([str(book) for book in self.total_books.values()])
        return f"[%d, t: %d, c: %d -> %s]" % (self.lib_id, self.signup, self.capacity, books)



class Lib(Interpretation):

    def __init__(self, all_libs: Dict[int, Library], all_books: Dict[int, Book], deadline: int) -> None:
        super().__init__()
        self.max_neigh = 8
        self.all_books: Dict[int, Book] = all_books
        self.all_libs: Dict[int, Library] = all_libs
        self.deadline: int = deadline
        self.picked_libs: Dict[int, Library] = {}

    def get_all_picked_books(self) -> Dict[int, Book]:
        picked_books = reduce(lambda x, y: x + y, [lib.picked_books for lib in self.picked_libs.values()])
        return dict([(book.book_id, book) for book in picked_books])

    def get_random_lib(self) -> Optional[Library]:
        libs = list(set(self.all_libs.values()).difference(self.picked_libs.values()))
        if len(libs) == 0:
            return None
        return random.choice(libs)

    def get_random_interpretation(self) -> Interpretation:
        self.picked_libs = {}
        for lid, library in self.all_libs.items():
            self.all_libs[lid].picked_books = []
        in_signup: int = -1
        in_scanning: List[Library] = []
        for day in range(self.deadline):
            if in_signup == -1:
                lib = self.get_random_lib()
                if lib is not None:
                    in_signup = lib.lib_id
            else:
                lib = self.all_libs[in_signup]
                lib.signup -= 1
                if lib.signup == 0:
                    lib.signup = lib.default_signup
                    lib.sort_books()
                    self.picked_libs[lib.lib_id] = lib
                    in_scanning.append(lib)
                    in_signup = -1
            for lib in in_scanning:
                lib_id = lib.lib_id
                bag = 0
                for bid, book in lib.total_books.items():
                    if lib.capacity == bag:
                        break
                    if bid not in self.get_all_picked_books():
                        bag += 1
                        self.picked_libs[lib_id].picked_books.append(book)
                        if len(lib.picked_books) == len(lib.total_books):
                            in_scanning.remove(lib)
        return self

    def add_not_picked_books(self, day, lib: Library):
        picked_books = self.get_all_picked_books()
        acc_day, bag = lib.signup, 0
        for b_id, book in lib.total_books.items():
            if b_id not in picked_books:
                if lib.capacity == bag:
                    bag = 0
                    acc_day += 1
                if acc_day + day == self.deadline:
                    break

    def all_score(self) -> int:
        all_sc = sum([book.score for book in self.all_books.values()])
        return all_sc

    def cost(self) -> int:
        all_sc = self.all_score()
        c_sc = self.score()
        return all_sc - c_sc

    def copy(self) -> Lib:
        c = Lib(self.all_libs.copy(), self.all_books.copy(), self.deadline)
        c.picked_libs = self.picked_libs.copy()
        return c

    def print(self, file_out: TextIO) -> None:
        sys.stderr.write("=========")
        good_libs = [lib for _, lib in self.picked_libs.items() if len(lib.picked_books) != 0]
        file_out.write(str(len(self.picked_libs)) + '\n')
        for library in good_libs:
            if len(library.picked_books) != 0:
                file_out.write(str(library.lib_id) + ' ' + str(len(library.picked_books)) + '\n')
                books = " ".join([str(book.book_id) for book in library.picked_books])
                file_out.write(books + '\n')
        sys.stderr.write("S'ha trobat solució\n")
        sys.stderr.write("COST: ==> " + str(self.cost()) + '\n')
        sys.stderr.write("SCORE: ==> " + str(self.score()) + '\n')
        sys.stderr.write("=========\n")

    def _get_list_neighbors(self) -> List[Interpretation]:
        res = []
        for i in range(self.max_neigh):
            neigh: Lib = self.copy()
            random.choice(list(self.picked_libs.items()))
            random.choice(list(self.picked_libs.items()))
            res.append(neigh)
        return res

    def get_best_neighbor(self) -> Interpretation:
        pass

    def get_random_walk(self) -> List[Interpretation]:
        pass

    def score(self) -> int:
        res = 0
        for _, library in self.picked_libs.items():
            res += sum([book.score for book in library.picked_books])
        return res


def main(data_id: int = 0, file_p: str = "/home/oriol/universitat/hashcode/book-hashcode/localsearch/a.txt"):
    from localsearch.srandom import Solver
    datasetURLs = [
        "https://hashcodejudge.withgoogle.com/download/blob/AMIfv96z2wILTmc0q35abZk6s8nklnGSRLd0IKa2jein6k8THmQLBlLCj144Yi8ih04jwPxn0ubGUsOWVha5w7UOMt0oLsSYtafv_oqVogstm7ve0br1JiNJ8IRE55Fgq2i6zRGNCTwjOU0gJJuRvevzTcP2Cq8_l5f9UcHJbfOfB0sq4evSBNx8gBMXZzNLUfpKppv848Z4XQ2Eh6e6qwfZO2QXbGnjnxuWNBDXYzdiMYd6CHI6qIHmY9K8pr81n4IaR9nF0_uESJ87ckK0lkNSX1c5VpCCfDxmVCM6DyYr2uWzEv15FKB0z0grxBdIy7Ek0M_L5GdR",
        "https://hashcodejudge.withgoogle.com/download/blob/AMIfv94kPv9bNHpmvuYRrlBfNhpxJTP3rqdEnAvWKPOmvlXWKTh4B3r-zEpdPVLqCmRr2a2U6NlmOseGUaKgA2MBL1R0smk2Yp5T4BBM5ksZ1ORlFESooGzvy7FMkB8QdideiU7DRpYIMBZ9n6iPDrJFYwWcvCa0lHkvFJkNVDhewrTmeunr24d_LaIVyKZ0DUiD9LSRFQXdG7aHc_7mnNPsv9j0l4LZCpFgdPDuA_i3Iowsi-dw7Jz9jiXhUO24DPm7iHoTqTB6hYGnkR-sUl1AJjFWa7q4xbe2EI3gh-ctcvdrIP92gE60ALO_-K57K6-esBJiYVqx",
        "https://hashcodejudge.withgoogle.com/download/blob/AMIfv95NC_WFM6Jsbq9RYjiBXGn1NaSHn6ZUu2NGyX_ez-9YgExaDbROx5QHPAb5UbBCOj4JXU25gZZN0a-q7x_CqqtG9DfLsewBlNb-bGTpBidu1rGh8UWRVB8P4z39RUaZYu3C7UuhE9WF4aUUmA1Xq847HKJDqJ22ksunXBGAnYI61yglZp_wOyzmdp0i_tRSmlO-Jj60bzgB084z3GUYfy00_Kih1c0f7g3iHIPr4FjlxY_4s4rZcJp29yrJHp_dDGZPGsK65tmtmK5c1kptuin39knpKc0tQ2hmJhV-YBNtvyVCvc-wVoM-0f4GsSCbUMnGmu-r",
        "https://hashcodejudge.withgoogle.com/download/blob/AMIfv94EswDoarsD_T8xfMl8Lx_Bb1V9ppyCMQuCsTXwowKBQ_JFwr9PzEVxgeAgwIeUbZU6R6sg2vrGKpBVKjpwfRfqJxFHOEobK82DVjKwLgi5jkGw3W3td09e18wF_xRXHtC2vewVhS0CyLoju7ykI9qLhZlaJI5ITzOSEKsPlT5sgkjCPFMK10ebbniYT4wKFAFGEMLkIolRCkgVAO0Fo2J20yNbrHbYkzZGbPS7Hq84DRX4rng0sT-HUXTYzZmRtzneJEg8-KD6vIJi4cCr8x4GgspQl_nZzCvnQ8If3PMDiFoqWF5JXW6ZjrpZWO9w6KTtvJAv",
        "https://hashcodejudge.withgoogle.com/download/blob/AMIfv94DTMLimuIhJSCxbRWjE9-zrgGFV3pPJJn6Gdt5z8qw4xGLbPyCSmfbkm7OXiWDTqVLV_KMGcYGDghaDnaAVLeooSukTi-ISm-NwZrbyYD_Mme7oF0i4BgDot0jbzE3aeBPa2jQSAjrGl3Rn7HAf1zmI875X5hPKxfOAie4JhY1ilZ259Ws5dm-16pZEVCON0qOqJyp1otWRLvkS1ik-E4viEB0ZAGANfwGEGCaFBFw6BP-5s-qQJwEFhcSkMOt_yoqo-Kh48eSl53aIy4wt9Wv5sgDt6dNgpg8i-ZZD9MJ8ZdNf-YShMvAhTf268TUaScyv3WIç",
        "https://hashcodejudge.withgoogle.com/download/blob/AMIfv97dgUsRkZX-sPN6ZjxVuupAVdZtpeLNfh2m1Y1brcUXLNq4SuwjqPA8Adl4FcNRewazJSiXfhQxjlgUNOnxlSF9hJxJdBzl2LIthcs2VBrD41rNUtd077k277McQLMFgwx1qPjvwnynXnUAZqE3F8XiTq9uOpAWSuMW1h8nbJwNCDcrH3-0ZPxW-3AGbozbJw6jWpCYuF2Gsq5Ato2ijJtI_hq9_7Oj37ddoFsYXOJnLO0toEK-hP4c9ItPQWm4SvrI3X2NPckkP15ImXsUhFXohgj-ZaudpG7he0X4oqpWoLAzJ3M0UyfMKHF5P9O1bLU-yi-8"
    ]
    from localsearch.currentdataset import Dataset
    d = Dataset(datasetURLs[data_id])
    total_score = sum([book.score for book in d.books])
    hash_books = {}
    for book in d.books:
        hash_books[book.book_id] = book
    hash_lib = {}
    for lib in d.libraries:
        hash_lib[lib.lib_id] = lib
    print('ACTUAL PROBLEM: ' + str(d.total_days))
    for lib in d.libraries:
        print(str(lib))
    lib = Lib(hash_lib, hash_books, d.total_days)
    solver = Solver(lib)
    solver.solve(10000000, file_p)
    # solver.solve(1000, 9000000, 0.1, file_p)


if __name__ == '__main__':
    main()
