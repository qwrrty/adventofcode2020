#! /usr/bin/env python3


def get_puzzle_input(filename="input.txt"):
    with open(filename, "r") as f:
        text = f.read()
    return text


def part1(text):
    groups = text.split("\n\n")

    # Go through each group and find all common answers
    total = 0
    for g in groups:
        all_answers = set()
        forms = g.split("\n")
        for f in forms:
            all_answers = all_answers.union(set(f))
        total += len(all_answers)

    return total


def part2(text):
    groups = text.split("\n\n")

    # Go through each group and find all common answers
    total = 0
    for g in groups:
        all_answers = set("abcdefghijklmnopqrstuvwxyz")
        forms = g.strip().split("\n")
        for f in forms:
            all_answers = all_answers.intersection(set(f))
            print("form {} / all_answers = {}".format(f, all_answers))
        print("total = {}".format(len(all_answers)))
        print("")
        total += len(all_answers)

    return total


if __name__ == "__main__":
    text = get_puzzle_input()
    result = part2(text)
    print(result)
