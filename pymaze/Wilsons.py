import random

from .DistancesGrid import DistancesGrid


class Wilsons(DistancesGrid):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        unvisited = [cell for cell in self]

        first = random.choice(unvisited)
        unvisited.remove(first)

        while unvisited:
            cell = random.choice(unvisited)
            path = [cell]

            while cell in unvisited:
                cell = random.choice(cell.neighbors())
                position = None if cell not in path else path.index(cell)

                if position is not None:
                    path = path[:position + 1]
                else:
                    path.append(cell)

            for (cell1, cell2) in zip(path, path[1:]):
                cell1.link(cell2)
                unvisited.remove(cell1)
