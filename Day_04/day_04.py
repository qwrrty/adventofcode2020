#! /usr/bin/env python3

import re


class Passport(object):

    _required_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid']
    
    def __init__(self, text):
        self.field = dict()
        for item in text.split():
            key, val = item.split(':')
            self.field[key] = val

    def get(self, key):
        return self.field.get(key)

    def byr_valid(text):
        try:
            byr = int(text)
        except ValueError:
            return False
        return 1920 <= byr <= 2002

    def iyr_valid(text):
        try:
            iyr = int(text)
        except ValueError:
            return False
        return 2010 <= iyr <= 2020

    def eyr_valid(text):
        try:
            iyr = int(text)
        except ValueError:
            return False
        return 2020 <= iyr <= 2030

    def hgt_valid(text):
        m = re.match(r"^(\d+)(cm|in)$", text)
        if m is None:
            return False
        hgt = int(m.group(1))
        if m.group(2) == "cm":
            return 150 <= hgt <= 193
        return 59 <= hgt <= 76

    def hcl_valid(text):
        return (re.match(r"^#[0-9a-f]{6}$", text) is not None)

    def ecl_valid(text):
        return (text in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"})

    def pid_valid(text):
        return re.match(r"^\d{9}$", text) is not None

    _validators = {
        "byr": byr_valid,
        "iyr": iyr_valid,
        "eyr": eyr_valid,
        "hgt": hgt_valid,
        "hcl": hcl_valid,
        "ecl": ecl_valid,
        "pid": pid_valid,
        "cid": lambda x: True,
    }
    
    def is_valid(self, optional=[], strict=False):
        for f in self._required_fields:
            # Skip optional fields
            if f not in optional and f not in self.field:
                return False
            if strict and not self._validators[f](self.get(f)):
                return False
        return True


def test():
    test_data = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
"""

    return part1(test_data)


def get_puzzle_input(filename="input.txt"):
    with open(filename, "r") as f:
        text = f.read()
    return text


def part1(data):
    total = 0
    for passport_text in data.split("\n\n"):
        p = Passport(passport_text)
        if p.is_valid(optional=["cid"]):
            total += 1

    return total


def part2(data):
    total = 0
    for passport_text in data.split("\n\n"):
        p = Passport(passport_text)
        if p.is_valid(optional=["cid"], strict=True):
            total += 1

    return total


if __name__ == '__main__':
    input_text = get_puzzle_input()
    print(part2(input_text))
