from enum import Enum

from .Grid import Grid


class DistancesGrid(Grid):
    class DistMatType(Enum):
        OFF = 0
        ON = 1
        SOL = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._distances = None
        self._distance_matrix = None
        self._solution = None

    @property
    def start(self):
        return super().start

    @start.setter
    def start(self, cell):
        super(DistancesGrid, self.__class__).start.fset(self, cell)
        self._distance_matrix = cell.distances()
        if self.end:
            self._solution = self._distance_matrix.path_to(self.end)

    @property
    def end(self):
        return super().end

    @end.setter
    def end(self, cell):
        super(DistancesGrid, self.__class__).end.fset(self, cell)
        if self.start:
            self._solution = self._distance_matrix.path_to(cell)

    @property
    def distances(self):
        return self._distances

    @distances.setter
    def distances(self, mode):
        if mode == self.DistMatType.OFF:
            self._distances = None
        elif mode == self.DistMatType.ON:
            self._distances = self._distance_matrix
        elif mode == self.DistMatType.SOL:
            self._distances = self._solution
        else:
            self._distances = None

    def set_longest_path(self):
        distances = self[0, 0].distances()
        self.start, _ = distances.max()
        self.end, _ = self._distance_matrix.max()
