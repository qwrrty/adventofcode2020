#! /usr/bin/env python

import re


def get_puzzle_input(filename="input.txt"):
    with open(filename, "r") as f:
        x = f.readlines()
    return x


def parse_passwd(p):
    r = re.match(r"^(\d+)-(\d+) (\w): (\w+)$", p)

    lo = int(r.group(1))
    hi = int(r.group(2))
    ltr = r[3]
    passwd = r[4]

    return (lo, hi, ltr, passwd)


def valid_password_letter_count(p):
    min_count, max_count, ltr, passwd = parse_passwd(p)

    # count the occurences of ltr in passwd
    ltr_count = sum(1 for x in passwd if x == ltr)

    return min_count <= ltr_count <= max_count


def valid_password_letter_position(p):
    lo, hi, ltr, passwd = parse_passwd(p)

    total = 0
    if passwd[lo-1] == ltr:
        total += 1
    if passwd[hi-1] == ltr:
        total += 1
    return total == 1


def part1():
    total = sum(1 for p in get_puzzle_input() if valid_password_letter_count(p))
    return total


def part2():
    total = sum(1 for p in get_puzzle_input() if valid_password_letter_position(p))
    return total


if __name__ == "__main__":
    result = part2()
    print(result)
