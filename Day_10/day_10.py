#! /usr/bin/env python3

from collections import defaultdict


def get_puzzle_input(filename="input.txt"):
    with open(filename, "r") as f:
        text = f.read()
    return text


def joltage_chain(input_data):
    adapters = []
    for line in input_data.split("\n"):
        if line:
            adapters.append(int(line))
    return sorted(adapters)


def part1(text):
    jolt = joltage_chain(text)
    jolt.insert(0, 0)
    jolt.append(jolt[-1] + 3)
    diff_counts = defaultdict(int)
    for i in range(1, len(jolt)):
        diff = jolt[i]-jolt[i-1]
        diff_counts[diff] += 1
    return diff_counts


def count_combos(chain, memo={}):
    if not chain:
        return 0

    # If there is only one adapter in the chain then there
    # is only one way to connect it to the device
    if len(chain) == 1:
        return 1

    # Otherwise start with the first adapter in the chain
    # and recursively add up the combinations it can be
    # added to
    combos = 0
    c = chain[0]

    # Have we memoized the number of combos achievable from this adapter?
    if c in memo:
        return memo[c]

    # Nope, better compute them
    for i in range(1, len(chain)):
        if chain[i] - c <= 3:
            combos += count_combos(chain[i:])
        else:
            break

    memo[c] = combos
    return combos


def part2(text):
    jolt = joltage_chain(text)
    jolt.insert(0, 0)
    jolt.append(jolt[-1] + 3)
    return count_combos(jolt)


test_input = """16
10
15
5
1
11
7
19
6
12
4"""


if __name__ == "__main__":
    text = get_puzzle_input("input.txt")
    result = part2(text)
    print(result)
