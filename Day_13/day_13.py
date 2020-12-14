#! /usr/bin/env python3

def get_puzzle_input(filename="input.txt"):
    with open(filename, "r") as f:
        text = f.read()
    return text


def part1(text):
    lines = text.split("\n")
    timestamp = int(lines[0])
    schedule = [int(x) for x in lines[1].split(",") if x.isdigit()]

    # For each bus route, find out how soon after the desired timestamp
    # it arrives
    #
    # That will be route - (timestamp % route) minutes
    #
    # since timestamp % route is the number of minutes since the _last_
    # bus on that route arrived

    waiting_times = {}
    for route in schedule:
        wait = route - (timestamp % route)
        waiting_times[wait] = route

    shortest = min(waiting_times.keys())
    return shortest * waiting_times[shortest]


# The brute force solution to part 2 will not finish in anything like
# a reasonable interval.

def part2(text):
    lines = text.split("\n")
    schedule = [int(x) if x.isdigit() else None for x in lines[1].split(",")]

    done = False
    ts = 0
    while not done:
        ts = ts + schedule[0]

        for i in range(1, len(schedule)):
            if schedule[i]:
                # The bus on this route must leave i minutes
                # after the first bus in the schedule
                if (ts + i) % schedule[i] != 0:
                    break
        else:
            # All bus schedules work, this timestamp is good
            done = True

    return ts


if __name__ == "__main__":
    text = get_puzzle_input("input.txt")
    print(part2(text))
