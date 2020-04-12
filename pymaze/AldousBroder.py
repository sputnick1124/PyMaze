import random

from .DistancesGrid import DistancesGrid


class AldousBroder(DistancesGrid):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cell = self.random_cell()
        unvisited = self.size() - 1

        while unvisited:
            neighbor = random.choice(cell.neighbors())

            if not neighbor.links:
                cell.link(neighbor)
                unvisited -= 1

            cell = neighbor
