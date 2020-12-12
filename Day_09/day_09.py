#! /usr/bin/env python3


class XmasCipher(object):

    def __init__(self, cipher_length):
        self.cipher_length = cipher_length
        self.data = []
        self.bad_sums = {}

    def validate(self, n):
        for i in range(-self.cipher_length, 0):
            for j in range(i+1, 0):
                if n == self.data[i] + self.data[j]:
                    return True
        return False

    def ingest(self, n):
        if len(self.data) >= self.cipher_length:
            if not self.validate(n):
                return False
        self.data.append(n)

        # Now compute sums of contiguous numbers that include n
        # for error checking in part 2
        for i in range(1, len(self.data)):
            bad_sum = sum(self.data[-i:])
            self.bad_sums[bad_sum] = self.data[-i:]

        return True


def get_puzzle_input(filename="input.txt"):
    with open(filename, "r") as f:
        text = f.read()
    return text


test_input = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""


def test():
    x = XmasCipher(5)
    for line in test_input.split("\n"):
        n = int(line)
        if not x.ingest(n):
            return n
    return 0


def part1(data):
    x = XmasCipher(25)
    for line in data.split("\n"):
        n = int(line)
        if not x.ingest(n):
            return n
    raise ValueError("all input passed")


def part2(data):
    x = XmasCipher(25)
    for line in data.split("\n"):
        n = int(line)
        if not x.ingest(n):
            return min(x.bad_sums[n]) + max(x.bad_sums[n])
    raise ValueError("all input passed")


if __name__ == "__main__":
    data = get_puzzle_input("input.txt")
    result = part2(data)
    print(result)
