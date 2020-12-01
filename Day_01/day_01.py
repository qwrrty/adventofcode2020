#! /usr/bin/env python


def get_puzzle_input(filename="input.txt"):
    with open(filename, "r") as f:
        x = f.readlines()
    return x


def part1():
    expenses = [int(x) for x in get_puzzle_input()]

    for i, a in enumerate(expenses):
        for j, b in enumerate(expenses, start=i+1):
            if a + b == 2020:
                return a * b

    # If we got here, we did not find any pair adding to 200
    print("No values found")
    raise Exception


def part2():
    expenses = [int(x) for x in get_puzzle_input()]

    for i, a in enumerate(expenses):
        for j, b in enumerate(expenses, start=i+1):
            for k, c in enumerate(expenses, start=j+1):
                if a + b + c == 2020:
                    return a * b * c

    # If we got here, we did not find any pair adding to 200
    print("No values found")
    raise Exception

    
if __name__ == "__main__":
    answer = part1()
    print(answer)
