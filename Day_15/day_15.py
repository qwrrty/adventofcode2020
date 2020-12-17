#! /usr/bin/env python3

from collections import defaultdict


class MemoryGame(object):

    def __init__(self, starting):
        self.turn = 0
        self.numbers = []
        self.turn_history = defaultdict(list)

        for n in starting:
            self.speak(n)

    def speak(self, n):
        self.turn += 1
        self.numbers.append(n)
        self.turn_history[n].append(self.turn)

    def next(self):
        n = self.numbers[-1]
        if len(self.turn_history[n]) > 1:
            # This number had been spoken before
            age = self.turn_history[n][-1] - self.turn_history[n][-2]
            self.speak(age)
        else:
            self.speak(0)


def part1(text):
    starting_numbers = [int(n) for n in text.split(",")]
    g = MemoryGame(starting_numbers)
    while g.turn < 2020:
        g.next()
    return g.numbers[-1]


def part2(text):
    starting_numbers = [int(n) for n in text.split(",")]
    g = MemoryGame(starting_numbers)
    while g.turn < 30000000:
        g.next()
    return g.numbers[-1]


if __name__ == "__main__":
    puzzle_input = "1,17,0,10,18,11,6"
    print(part1(puzzle_input))
