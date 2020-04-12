import random

from .DistancesGrid import DistancesGrid


class Sidewinder(DistancesGrid):
    def __init__(self, rows, cols, **kwargs):
        super().__init__(rows, cols, **kwargs)
        for row in self.iter_rows():
            run = []
            for cell in row:
                run.append(cell)

                at_eastern_bound = cell.east is None
                at_northern_bound = cell.north is None

                should_close_out = (at_eastern_bound or
                                    (not at_northern_bound and
                                     random.randint(0, 2) == 0))

                if should_close_out:
                    member = random.choice(run)
                    if member.north:
                        member.link(member.north)
                    run = []
                else:
                    cell.link(cell.east)
