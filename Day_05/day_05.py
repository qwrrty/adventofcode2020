#! /usr/bin/env python3


class BoardingPass(object):

    def __init__(self, text):
        # Instead of zones or groups, this airline uses binary space
        # partitioning to seat people. A seat might be specified like
        # FBFBBFFRLR, where F means "front", B means "back", L means
        # "left", and R means "right".
        #
        # The first 7 characters will either be F or B; these specify
        # exactly one of the 128 rows on the plane (numbered 0 through
        # 127). Each letter tells you which half of a region the given
        # seat is in. Start with the whole list of rows; the first
        # letter indicates whether the seat is in the front (0 through
        # 63) or the back (64 through 127). The next letter indicates
        # which half of that region the seat is in, and so on until
        # you're left with exactly one row.
        #
        # The last three characters will be either L or R; these
        # specify exactly one of the 8 columns of seats on the plane
        # (numbered 0 through 7). The same process as above proceeds
        # again, this time with only three steps. L means to keep the
        # lower half, while R means to keep the upper half.

        self.row = 0
        self.col = 0

        row_str = text[:7]
        col_str = text[7:]

        for c in row_str:
            self.row = self.row * 2 + (1 if c == 'B' else 0)

        for c in col_str:
            self.col = self.col * 2 + (1 if c == 'R' else 0)

        self.seat_id = self.row * 8 + self.col

    def __repr__(self):
        return "<BoardingPass row={} col={} seat_id={}>".format(
            self.row, self.col, self.seat_id)


def get_puzzle_input(filename="input.txt"):
    with open(filename, "r") as f:
        input_data = [line.rstrip() for line in f]
    return input_data


def part1(filename="input.txt"):
    data = get_puzzle_input(filename)
    highest_bp = max(BoardingPass(x).seat_id for x in data)
    return highest_bp


def part2(filename="input.txt"):
    data = get_puzzle_input(filename)
    bps = [BoardingPass(x) for x in data]

    # Build a map of all seats on the aircraft
    # and remove each one that's present in the
    # input data. Of the remaining keys, the one
    # where neither of its neighbors is present
    # will be our seat.
    #
    # Sort of conceptually lazy, but efficient
    # inasmuch as it makes the search space
    # very small.

    highest_bp = max(x.seat_id for x in bps)
    all_seats = {x: True for x in range(0, highest_bp+1)}
    for x in bps:
        del all_seats[x.seat_id]
    for x in all_seats:
        if x-1 not in all_seats and x+1 not in all_seats:
            return x
    return None


if __name__ == "__main__":
    result = part2()
    print(result)
