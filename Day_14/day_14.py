#! /usr/bin/env python3

import re


def get_puzzle_input(filename="input.txt"):
    with open(filename, "r") as f:
        text = f.read()
    return text


class DockingProgram(object):

    def __init__(self):
        self.memory = {}
        self.and_mask = 0b11111111111111111111111111111111111
        self.or_mask = 0

    def __repr__(self):
        return "<DockingProgram and_mask={:b} or_mask={:b}>".format(
            self.and_mask,
            self.or_mask,
        )

    def process(self, line):
        m = re.match(r"^mask\s*=\s*([X10]*)", line)
        if m:
            maskstr = m.group(1)
            self.and_mask = int(re.sub(r"[^0]", "1", maskstr), base=2)
            self.or_mask = int(re.sub(r"[^1]", "0", maskstr), base=2)
            return
        m = re.match(r"^mem\[(\d+)\]\s*=\s*(\d+)", line)
        if m:
            addr = int(m.group(1))
            val = int(m.group(2))
            self.memory[addr] = val & self.and_mask | self.or_mask
            return
        raise ValueError(line)

    def run(self, text):
        for line in text.split("\n"):
            if line:
                self.process(line)

    def memory_sum(self):
        return sum(self.memory.values())


class DockingProgramV2(object):

    def __init__(self):
        self.memory = {}
        self.mask = ""

    def apply_mask(self, n):
        n_binary = "{:036b}".format(n)
        masksize = self.mask.count("X")
        fmt = "{:0%db}" % masksize

        results = []
        
        # Enumerate all the possible masks corresponding
        # to the Xs in the current mask string.
        for mask in range(2 ** masksize):
            maskbits = fmt.format(mask)
            b = 0
            result_bits = []
            for bit in range(36):
                if self.mask[bit] == "X":
                    result_bits.append(maskbits[b])
                    b += 1
                elif self.mask[bit] == "1":
                    result_bits.append("1")
                else:
                    result_bits.append(n_binary[bit])
            results.append("".join(result_bits))

        return [int(n, base=2) for n in results]

    def process(self, line):
        m = re.match(r"^mask\s*=\s*([X10]*)", line)
        if m:
            self.mask = m.group(1)
            return
        m = re.match(r"^mem\[(\d+)\]\s*=\s*(\d+)", line)
        if m:
            addr = int(m.group(1))
            val = int(m.group(2))
            addrs = self.apply_mask(addr)
            for a in addrs:
                self.memory[a] = val
            return
        raise ValueError(line)

    def run(self, text):
        for line in text.split("\n"):
            if line:
                self.process(line)

    def memory_sum(self):
        return sum(self.memory.values())


def part1(text):
    p = DockingProgram()
    p.run(text)
    return p.memory_sum()


def part2(text):
    p = DockingProgramV2()
    p.run(text)
    return p.memory_sum()


if __name__ == "__main__":
    text = get_puzzle_input("input.txt")
    print(part2(text))
