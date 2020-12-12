#! /usr/bin/env python3

from enum import IntEnum


def get_puzzle_input(filename="input.txt"):
    with open(filename, "r") as f:
        text = f.read()
    return text


class Direction(IntEnum):
    EAST = 0
    SOUTH = 1
    WEST = 2
    NORTH = 3

    def compass(val):
        if val == "N" or val == "NORTH":
            return Direction.NORTH
        elif val == "S" or val == "SOUTH":
            return Direction.SOUTH
        elif val == "W" or val == "WEST":
            return Direction.WEST
        elif val == "E" or val == "EAST":
            return Direction.EAST
        else:
            raise ValueError("invalid initializer {}".format(val))


class Ship(object):

    def __init__(self):
        self.direction = Direction.EAST
        self.xpos = 0
        self.ypos = 0

    def __repr__(self):
        return "<Ship {!s} pos=({},{})>".format(
            self.direction,
            self.xpos,
            self.ypos,
        )

    def turn(self, direction, degrees):
        degrees /= 90
        if direction == "L":
            degrees = -degrees
        self.direction = Direction((self.direction + degrees) % 4)

    def move(self, direction, count):
        xd = 0
        yd = 0
        if direction == "F":
            direction = self.direction
        else:
            direction = Direction.compass(direction)

        if direction == Direction.NORTH:
            yd = -count
        elif direction == Direction.SOUTH:
            yd = count
        elif direction == Direction.EAST:
            xd = count
        elif direction == Direction.WEST:
            xd = -count

        self.xpos += xd
        self.ypos += yd


class ShipWaypoint(object):

    def __init__(self):
        self.xpos = 0
        self.ypos = 0
        self.waypoint_x = 10
        self.waypoint_y = -1

    def __repr__(self):
        return "<ShipWaypoint pos=({},{}) waypoint=({},{})>".format(
            self.xpos,
            self.ypos,
            self.waypoint_x,
            self.waypoint_y,
        )

    # 10, -4  - northeast
    #  4, 10  - southeast
    # -10, 4  - southwest
    # -4, -10 - northwest
    #
    # When turning R:
    #   - new X is negative if old Y was positive
    #   - new Y is negative if old X was negative
    # When turning L:
    #   - new X is negative if old Y was negative
    #   - new Y is negative if old X was positive
    
    def move(self, direction, argument):
        if direction == "F":
            self.xpos += self.waypoint_x * argument
            self.ypos += self.waypoint_y * argument
        elif direction == "N":
            self.waypoint_y -= argument
        elif direction == "S":
            self.waypoint_y += argument
        elif direction == "E":
            self.waypoint_x += argument
        elif direction == "W":
            self.waypoint_x -= argument
        elif direction == "L":
            while argument > 0:
                new_x = abs(self.waypoint_y)
                new_y = abs(self.waypoint_x)
                if self.waypoint_y < 0:
                    new_x = -new_x
                if self.waypoint_x > 0:
                    new_y = -new_y
                self.waypoint_x = new_x
                self.waypoint_y = new_y
                argument -= 90
        elif direction == "R":
            while argument > 0:
                new_x = abs(self.waypoint_y)
                new_y = abs(self.waypoint_x)
                if self.waypoint_y > 0:
                    new_x = -new_x
                if self.waypoint_x < 0:
                    new_y = -new_y
                self.waypoint_x = new_x
                self.waypoint_y = new_y
                argument -= 90
        else:
            raise ValueError("unknown direction {}".format(direction))


def part1(directions):
    s = Ship()
    for line in directions.split("\n"):
        if not line:
            continue
        direction = line[0]
        arg = int(line[1:])
        if direction in {"L", "R"}:
            s.turn(direction, arg)
        elif direction in {"N", "S", "E", "W", "F"}:
            s.move(direction, arg)
        else:
            raise ValueError(line)

    return abs(s.xpos) + abs(s.ypos)


def part2(directions):
    s = ShipWaypoint()
    for line in directions.split("\n"):
        if not line:
            continue
        direction = line[0]
        arg = int(line[1:])
        s.move(direction, arg)

    return abs(s.xpos) + abs(s.ypos)


def test():
    test_input = """F10
N3
F7
R90
F11"""
    result = part2(test_input)
    return result


if __name__ == "__main__":
    data = get_puzzle_input("input.txt")
    print(part2(data))
