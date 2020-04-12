import random

from .DistancesGrid import DistancesGrid


class HuntAndKill(DistancesGrid):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current = self.random_cell()

        while current is not None:
            unvisited_neighbors = [n for n in current.neighbors() if not n.links]

            if unvisited_neighbors:
                neighbor = random.choice(unvisited_neighbors)
                current.link(neighbor)
                current = neighbor
            else:
                current = None

                for cell in self:
                    visited_neighbors = [n for n in cell.neighbors() if n.links]
                    if not cell.links and visited_neighbors:
                        current = cell

                        neighbor = random.choice(visited_neighbors)
                        current.link(neighbor)

                        break
