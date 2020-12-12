#! /usr/bin/env python3

import re

test_input = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
"""


def get_puzzle_input(filename="input.txt"):
    with open(filename, "r") as f:
        text = f.read()
    return text


def parse_color_rules(text):
    color_rules = dict()
    for rule in text.split("\n"):
        # Skip empty lines
        if not rule:
            continue
        m = re.match(r"^(.*) bags contain (.*)\.$", rule)
        bag_color = m.group(1)
        color_rules[bag_color] = {}
        if m.group(2) == "no other bags":
            continue
        subbags = m.group(2).split(", ")
        for b in subbags:
            m2 = re.match(r"^(\d+) (.*) bags?$", b)
            sub_quantity = int(m2.group(1))
            sub_color = m2.group(2)
            color_rules[bag_color][sub_color] = sub_quantity
    return color_rules


def may_contain(bag_color, color_rules, desired_bag_color):
    # Check to see if a bag_color bag can contain a
    # bag of desired_bag_color, either directly or
    # indirectly
    #
    # Note that if bag_content_options included
    # any mutual color loops (e.g. a bright white
    # bag may contain a faded blue bag, and faded
    # blue bag may contain bright white bags) then
    # we would need additional logic to avoid infinite
    # recursive loops.
    for color in color_rules[bag_color]:
        if color == desired_bag_color:
            return True
        if may_contain(color, color_rules, desired_bag_color):
            return True
    return False


def part1(bag_color_rules):
    valid_colors = [color
                    for color in bag_color_rules
                    if may_contain(color, bag_color_rules, "shiny gold")]
    return len(valid_colors)


def count_bags(bag_color, bag_color_rules):
    count = 0
    for color, quantity in bag_color_rules[bag_color].items():
        count = count + quantity + quantity * count_bags(color, bag_color_rules)
    return count


def part2(bag_color_rules):
    return count_bags("shiny gold", bag_color_rules)


def test():
    from pprint import pprint
    color_rules = parse_color_rules(test_input)
    pprint(color_rules)


if __name__ == "__main__":
    text = get_puzzle_input()
    bag_color_rules = parse_color_rules(text)
    result = part2(bag_color_rules)
    print(result)
