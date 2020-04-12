import random

from .DistancesGrid import DistancesGrid


class BinaryTree(DistancesGrid):
    def __init__(self, rows, cols, **kwargs):
        super().__init__(rows, cols, **kwargs)
        for cell in self:
            neighbors = []
            if cell.east is not None:
                neighbors.append(cell.east)
            if cell.north is not None:
                neighbors.append(cell.north)

            neighbor = random.choice(neighbors) if neighbors else None
            if neighbor is not None:
                cell.link(neighbor)
