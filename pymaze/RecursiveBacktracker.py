import random

from .DistancesGrid import DistancesGrid


class RecursiveBacktracker(DistancesGrid):
    def __init__(self, *args, start_at=None, **kwargs):
        super().__init__(*args, **kwargs)
        if start_at is None:
            start_at = self.random_cell()
        stack = [start_at]

        while stack:
            current = stack[-1]
            neighbors = [n for n in current.neighbors() if not n.links]

            if not neighbors:
                stack.pop()
            else:
                neighbor = random.choice(neighbors)

                current.link(neighbor)
                stack.append(neighbor)
