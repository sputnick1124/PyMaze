#!/home/nick/.virtualenvs/pymaze/bin/python
import sys

from pymaze.Sidewinder import Sidewinder


def main():
    rows = int(sys.argv[1])
    cols = int(sys.argv[2])

    maze = Sidewinder(rows, cols)
    maze.set_longest_path()
    # maze.distances = maze.DistMatType.OFF
    maze.distances = maze.DistMatType.SOL

    print(maze)


if __name__ == "__main__":
    main()
