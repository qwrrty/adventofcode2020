#! /usr/bin/env python3


class TreeMap(object):
    def __init__(self, map_text):
        self.tree_map = map_text
        self.width = len(map_text[0])
        self.height = len(map_text)

    @staticmethod
    def from_file(filename):
        with open(filename, "r") as f:
            map_text = [x.rstrip() for x in f]
        return TreeMap(map_text)

    def tree_at(self, x, y):
        # Return True or False depending on whether there is a
        # tree at the specified coordinates

        return self.tree_map[y][x % self.width] == "#"

    def traverse(self, xdelta, ydelta):
        # Traverse a map, moving by xdelta and ydelta squares
        # at each step, counting the number of trees struck

        x = 0
        y = 0
        total = 0
        while y < self.height:
            if self.tree_at(x, y):
                total += 1
            x += xdelta
            y += ydelta

        return total


def part1(filename="input.txt"):
    t = TreeMap.from_file(filename)

    # Starting from 0,0, repeatedly travel right 3 and down 1
    # squares. Add 1 to the total number of trees hit each time
    # a tree is encountered.
    return t.traverse(xdelta=3, ydelta=1)


def part2(filename="input.txt"):
    t = TreeMap.from_file(filename)

    # Determine the number of trees you would encounter if, for each of the following slopes, you start at the top-left corner and traverse the map all the way to the bottom:
    #
    #   - Right 1, down 1.
    #   - Right 3, down 1. (This is the slope you already checked.)
    #   - Right 5, down 1.
    #   - Right 7, down 1.
    #   - Right 1, down 2.

    n1 = t.traverse(1, 1)
    n2 = t.traverse(3, 1)
    n3 = t.traverse(5, 1)
    n4 = t.traverse(7, 1)
    n5 = t.traverse(1, 2)

    return n1 * n2 * n3 * n4 * n5


if __name__ == "__main__":
    result = part2()
    print(result)
