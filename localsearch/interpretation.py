from __future__ import annotations

import random
from typing import List, TextIO


class Interpretation(object):

    def __init__(self):
        self.id = hash(self)

    def get_random_interpretation(self) -> Interpretation:
        raise NotImplementedError

    def cost(self) -> int:
        raise NotImplementedError

    def copy(self) -> Interpretation:
        raise NotImplementedError

    def print(self, file_out: TextIO) -> None:
        raise NotImplementedError

    def _get_list_neighbors(self) -> List[Interpretation]:
        raise NotImplementedError

    def get_best_neighbor(self) -> Interpretation:
        raise NotImplementedError

    def get_random_walk(self) -> List[Interpretation]:
        raise NotImplementedError
