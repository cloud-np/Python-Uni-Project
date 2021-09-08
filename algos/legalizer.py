from classes.node import Node
from typing import List, Tuple
from itertools import combinations


class Legalizer:

    @staticmethod
    def check_for_overlaps(cells: List[Node]) -> List[Tuple[Node]]:
        return [pair for pair in combinations(cells, 2) if pair[0].rectan.check_overlap(pair[1])]
