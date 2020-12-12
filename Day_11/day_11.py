#! /ust/bin/env python3


class Ferry(object):
    def __init__(self, seat_map):
        self.seat_map = []
        for row in seat_map.strip().split("\n"):
            self.seat_map.append(list(row))
        self.width = len(self.seat_map[0])
        self.height = len(self.seat_map)

    def vacant(self, x, y):
        return self.seat_map[y][x] == "L"

    def occupied(self, x, y):
        return self.seat_map[y][x] == "#"

    def occupied_count(self):
        count = 0
        for y in range(0, self.height):
            for x in range(0, self.width):
                if self.occupied(x, y):
                    count += 1
        return count

    def seat(self, x, y):
        return self.seat_map[y][x]

    def neighbors(self, x, y):
        count = 0
        for yd in [-1, 0, 1]:
            for xd in [-1, 0, 1]:
                # Skip the current cell
                if xd == 0 and yd == 0:
                    continue
                if 0 <= x + xd < self.width and 0 <= y + yd < self.height:
                    if self.occupied(x+xd, y+yd):
                        count += 1
        return count

    def visible_occupied(self, x, y):
        # Returns the number of occupied seats that are visible
        # from (x, y).

        count = 0
        # North
        for yd in range(y-1, -1, -1):
            if self.vacant(x, yd):
                break
            elif self.occupied(x, yd):
                count += 1
                break

        # West
        for xd in range(x-1, -1, -1):
            if self.vacant(xd, y):
                break
            elif self.occupied(xd, y):
                count += 1
                break

        # South
        for yd in range(y+1, self.height):
            if self.vacant(x, yd):
                break
            elif self.occupied(x, yd):
                count +=1
                break

        # East
        for xd in range(x+1, self.width):
            if self.vacant(xd, y):
                break
            elif self.occupied(xd, y):
                count += 1
                break

        # Northwest
        yd = y-1
        for xd in range(x-1, -1, -1):
            if yd < 0:
                break
            elif self.vacant(xd, yd):
                break
            elif self.occupied(xd, yd):
                count += 1
                break
            yd -= 1

        # Southwest
        yd = y+1
        for xd in range(x-1, -1, -1):
            if yd >= self.height:
                break
            elif self.vacant(xd, yd):
                break
            elif self.occupied(xd, yd):
                count += 1
                break
            yd += 1

        # Southeast
        yd = y+1
        for xd in range(x+1, self.width):
            if yd >= self.height:
                break
            elif self.vacant(xd, yd):
                break
            elif self.occupied(xd, yd):
                count += 1
                break
            yd += 1

        # Northeast
        yd = y-1
        for xd in range(x+1, self.width):
            if yd < 0:
                break
            elif self.vacant(xd, yd):
                break
            elif self.occupied(xd, yd):
                count += 1
                break
            yd -= 1

        return count

    def update(self, visible=False, neighbor_limit=4):
        new_map = []
        modified = False
        for y in range(0, self.height):
            row = []
            for x in range(0, self.width):
                # - If a seat is empty (L) and there are no occupied seats
                # adjacent to it, the seat becomes occupied.
                # - If a seat is occupied (#) and four or more seats adjacent
                # to it are also occupied, the seat becomes empty.
                if visible:
                    neighbors = self.visible_occupied(x, y)
                else:
                    neighbors = self.neighbors(x, y)

                if self.vacant(x, y) and neighbors == 0:
                    row.append("#")
                    modified = True
                elif self.occupied(x, y) and neighbors >= neighbor_limit:
                    row.append("L")
                    modified = True
                else:
                    row.append(self.seat(x, y))
            new_map.append(row)

        if modified:
            self.seat_map = new_map
        return modified

    def __str__(self):
        rows = ["".join(row) for row in self.seat_map]
        return "\n".join(rows)


def test():
    test_input = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""

    ferry = Ferry(test_input)
    print(ferry)


def get_puzzle_input(filename="input.txt"):
    with open(filename, "r") as f:
        text = f.read()
    return text


def part1(seat_map):
    f = Ferry(seat_map)
    while f.update():
        pass
    return f.occupied_count()


def part2(seat_map):
    f = Ferry(seat_map)
    while f.update(visible=True, neighbor_limit=5):
        pass
    return f.occupied_count()


if __name__ == "__main__":
    seat_map = get_puzzle_input("input.txt")
    print(part2(seat_map))
