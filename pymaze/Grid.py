import random
from string import ascii_letters, digits
from operator import itemgetter

from PIL import Image, ImageDraw

from .Cell import Cell, StrokeWeight
from .Distances import Distances


class Grid:
    def __init__(self, rows, cols, stroke_weight=StrokeWeight.Light):
        self.rows = rows
        self.cols = cols
        self._lw = stroke_weight

        self.grid = self.prepare_grid()
        self.configure_cells()

        self._cursor_col = 0
        self._cursor_row = 0

        self._start, self._end = None, None

    def prepare_grid(self):
        return [[
                    Cell(row, col, stroke_weight=self._lw) for col in range(self.cols)
                ] for row in range(self.rows)]

    def configure_cells(self):
        for cell in self:
            row, col = cell.row, cell.col

            cell.north = self[row - 1, col]
            cell.east = self[row, col + 1]
            cell.south = self[row + 1, col]
            cell.west = self[row, col - 1]

    def random_cell(self):
        row = random.choice(self.grid)
        return random.choice(row)

    def size(self):
        return self.rows*self.cols

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, cell):
        if self._start:
            self._start.start = False
        cell.start = True
        self._start = cell

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, cell):
        if self._end:
            self._end.end = False
        cell.end = True
        self._end = cell

    def iter_rows(self):
        for row in self.grid:
            yield row

    def __iter__(self):
        self._cursor_col = 0
        self._cursor_row = 0
        return self

    def __next__(self):
        if 0 <= self._cursor_row < self.rows:
            res = self[self._cursor_row, self._cursor_col]
            self._cursor_col += 1
            if self._cursor_col >= self.cols:
                self._cursor_col = 0
                self._cursor_row += 1
            return res
        else:
            raise StopIteration

    def __getitem__(self, row_col):
        row, col = row_col
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        else:
            return None

    def __repr__(self):
        return f"Grid(rows={self.rows}, cols={self.cols})"

    def __str__(self):
        d = self.distances if self.distances else {}
        return '\n'.join(
                   '\n'.join(
                       ''.join(f) for f in zip(*(c._tile(self.base_62(d.get(c))) for c in r))
                    ) for r in self.iter_rows()
                )

    @staticmethod
    def base_62(i=None):
        if i is None:
            return i
        res = ''
        digs = digits + ascii_letters
        while i:
            res += digs[i % 62]
            i //= 62
        return ''.join(reversed(res))

    def print_ascii(self):
        output = f"+{'---+'*self.cols}\n"

        for row in self.iter_rows():
            top = "|"
            bot = "+"

            for cell in row:
                if cell.start:
                    # body = " \ue000 "
                    body = f" {chr(0x1f464)}"
                elif cell.end:
                    body = f" {chr(0x2b50)}"
                else:
                    body = " "*3
                top += f"{body}{' ' if cell.linked(cell.east) else '|'}"

                corner = "+"
                bot += f"{(' ' if cell.linked(cell.south) else '-')*3}{corner}"
            output += f"{top}\n{bot}\n"
        return output

    def to_png(self, cell_size=10, colorize=False, solution=False):
        img_width = cell_size*self.cols
        img_height = cell_size*self.rows

        img = Image.new('P', (img_width, img_height), 255)
        draw = ImageDraw.Draw(img)

        d = self._distance_matrix if self._distance_matrix else {}

        for mode in range(2):
            for cell in self:
                x1 = cell.col*cell_size
                y1 = cell.row*cell_size
                x2 = (cell.col + 1)*cell_size
                y2 = (cell.row + 1)*cell_size

                if mode == 0 and colorize:
                    color = self.background_color_for(cell)
                    draw.rectangle((x1, y1, x2, y2), fill=color)
                else:
                    if cell.north is None:
                        draw.line((x1, y1, x2, y1), fill=0)
                    if cell.west is None:
                        draw.line((x1, y1, x1, y2), fill=0)
                    if not cell.linked(cell.east) or cell.east is None:
                        draw.line((x2, y1, x2, y2), fill=0)
                    if not cell.linked(cell.south) or cell.south is None:
                        draw.line((x1, y2, x2, y2), fill=0)

                bounding_box = ( x1 + cell_size//4, y1 + cell_size//4, x2 - cell_size//4, y2 - cell_size//4)
                if cell.start:
                    draw.ellipse(bounding_box, fill=255, outline=0)
                elif cell.end:
                    draw.ellipse(bounding_box, fill=0, outline=0)
        if solution and self._solution:
            solution_path = sorted(self._solution.items(), key=itemgetter(1))
            for ((cell1, _), (cell2, _)) in zip(solution_path, solution_path[1:]):
                x1 = (2*cell1.col + 1)*cell_size//2
                y1 = (2*cell1.row + 1)*cell_size//2
                x2 = (2*cell2.col + 1)*cell_size//2
                y2 = (2*cell2.row + 1)*cell_size//2

                draw.line((x1, y1, x2, y2), width=cell_size//4, fill=0)
        del draw
        return img

    def background_color_for(self, cell):
        if self._distance_matrix:
            _, max_distance = self._distance_matrix.max()
            return int(255*(max_distance - self._distance_matrix.get(cell, 0))/max_distance)
        else:
            return 255

    def deadends(self):
        return len([c for c in self if len(c.links) == 1])
