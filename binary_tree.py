#!/usr/bin/env python
import sys

from pymaze.BinaryTree import BinaryTree


def main():
    rows = int(sys.argv[1])
    cols = int(sys.argv[2])

    btree = BinaryTree(rows, cols)

    print(btree)


if __name__ == "__main__":
    main()
