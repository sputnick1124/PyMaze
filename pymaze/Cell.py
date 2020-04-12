from enum import Enum
from itertools import product

from wcwidth import wcwidth

from .Distances import Distances


class StrokeWeight(Enum):
    Light = 0
    Heavy = 1


class BoxChars:
    def __init__(self, stroke_weight: StrokeWeight):
        char_map = {
                'horiz': 0x2500 + stroke_weight.value,
                'vert': 0x2502 + stroke_weight.value,
                'tl_corner': 0x250c + stroke_weight.value*3,
                'tr_corner': 0x2510 + stroke_weight.value*3,
                'bl_corner': 0x2514 + stroke_weight.value*3,
                'br_corner': 0x2518 + stroke_weight.value*3,
                'l_junction': 0x251c + stroke_weight.value*7,
                'r_junction': 0x2524 + stroke_weight.value*7,
                't_junction': 0x252c + stroke_weight.value*7,
                'b_junction': 0x2534 + stroke_weight.value*7,
                'x_junction': 0x253c + stroke_weight.value*15
                }
        for (name, code) in char_map.items():
            setattr(self, name, chr(code))


class Cell:
    def __init__(self, row, col, stroke_weight=StrokeWeight.Light,
                 draw_start_end=True, start_char='0', end_char='*'):
        self.row = row
        self.col = col

        self.north = None
        self.east = None
        self.south = None
        self.west = None

        self._links = {}

        self.start = False
        self.end = False

        self._bc = BoxChars(stroke_weight)

        self.draw_start_end = draw_start_end
        self.start_char = start_char
        self.end_char = end_char

    def neighbors(self):
        return [n for n in [self.north, self.east, self.south, self.west] if n is not None]

    def distances(self):
        distances = Distances(self)
        frontier = {self}

        while frontier:
            new_frontier = set()
            for cell in frontier:
                for linked in cell.links:
                    if distances.get(linked) is None:
                        distances[linked] = distances[cell] + 1
                        new_frontier.add(linked)
            frontier = new_frontier

        return distances

    @property
    def links(self):
        return self._links

    def link(self, other, bidi=True):
        self._links[other] = True
        if bidi:
            other.link(self, False)

    def unlink(self, other, bidi=True):
        self._links[other] = False
        if bidi:
            other.unlink(self, False)

    def linked(self, other):
        return self._links.get(other, False)

    def _tile(self, name=None):
        name = name if name else " "
        neighbors = self.neighbors()
        tr_corner = ""
        bl_corner = ""
        br_corner = ""
        bot = ""

        # do the bits that are the same for all cells
        if not self.linked(self.north):
            top = self._bc.horiz*3
        else:
            top = " "*3

        if self.draw_start_end:
            if self.start:
                body = self.center_char(self.start_char)
            elif self.end:
                body = self.center_char(self.end_char)
            else:
                body = name.center(3)
        else:
            body = name.center(3)
        if not self.linked(self.west):
            body = self._bc.vert + body
        else:
            body = body + " "
        if self.east not in neighbors:
            body += self._bc.vert

        # handle corners for special cases of boundary walls
        if self.south not in neighbors:  # bottow row (south wall)
            if self.east not in neighbors:
                br_corner = self._bc.br_corner
            if self.west not in neighbors:
                bl_corner = self._bc.bl_corner
            elif self.linked(self.west):
                bl_corner = self._bc.horiz
            else:
                bl_corner = self._bc.b_junction
            bot = f"{bl_corner}{self._bc.horiz*3}{br_corner}"
        if self.north not in neighbors:  # top row (north wall)
            if self.west not in neighbors:  # top left corner
                corner = self._bc.tl_corner
            elif self.linked(self.west):
                corner = self._bc.horiz
            else:
                corner = self._bc.t_junction
            if self.east not in neighbors:
                tr_corner = self._bc.tr_corner
        elif self.west not in neighbors:  # first column (west wall)
            if self.linked(self.north):  # open on top
                corner = self._bc.vert
            else:
                corner = self._bc.l_junction
        else:
            if self.east not in neighbors:  # last column (east wall)
                if self.linked(self.north):
                    tr_corner = self._bc.vert
                else:
                    tr_corner = self._bc.r_junction
            # all the rest of the corners fall into one of 16 possibilities
            northwest = self.north.west
            condition = (self.north.linked(northwest), self.linked(self.north),
                         self.linked(self.west), self.west.linked(northwest))
            corners = (" ",
                       " ",
                       " ",
                       self._bc.tr_corner,
                       " ",
                       self._bc.horiz,
                       self._bc.tl_corner,
                       self._bc.t_junction,
                       " ",
                       self._bc.br_corner,
                       self._bc.vert,
                       self._bc.r_junction,
                       self._bc.bl_corner,
                       self._bc.b_junction,
                       self._bc.l_junction,
                       self._bc.x_junction)
            corner_map = {cnd: crnr for cnd, crnr in zip(product(*(((True, False),)*4)), corners)}
            corner = corner_map.get(condition)
        return (f"{corner}{top}{tr_corner}", body) if not bot else (f"{corner}{top}{tr_corner}", body, bot)

    def __str__(self):
        return f"Cell({self.row},{self.col})"

    def __repr__(self):
        links = [d for c, d in zip(
                                [self.north, self.east, self.south, self.west],
                                ["north", "east", "south", "west"])
                 if c in self.links.keys()]
        return f"Cell((row, col)=({self.row}, {self.col}), links={links})"

    @staticmethod
    def center_char(c, width=3):
        if wcwidth(c) > 1:
            return c.rjust(wcwidth(c) - width + 1)
        else:
            return c.center(width)
