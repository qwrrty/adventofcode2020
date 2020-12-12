#! /usr/bin/env python3


class Instruction(object):

    ACC = 1
    JMP = 2
    NOP = 3

    assembler = {
        "acc": ACC,
        "jmp": JMP,
        "nop": NOP,
    }

    decode = {
        ACC: "acc",
        JMP: "jmp",
        NOP: "nop",
    }

    def __init__(self, opcode, operand):
        self.opcode = Instruction.assembler[opcode.lower()]
        self.operand = int(operand)

    def __repr__(self):
        return "<Instruction {} {}>".format(
            Instruction.decode[self.opcode],
            self.operand
        )


class BootCode(object):

    def __init__(self, sourcecode):
        self.program = []
        self.accumulator = 0
        self.pc = 0
        for line in sourcecode.split("\n"):
            if not line:
                continue
            opcode, operand = line.split()
            self.program.append(Instruction(opcode, operand))

    def run(self):
        # Run until an infinite loop is reached, or the program terminates naturally
        # Return True if the program reached its natural end, False otherwise
        self.accumulator = 0
        pc = 0
        visited = {}
        while pc not in visited and pc < len(self.program):
            visited[pc] = True
            inst = self.program[pc]
            pc_step = 1
            if inst.opcode == Instruction.ACC:
                self.accumulator += inst.operand
            elif inst.opcode == Instruction.JMP:
                pc_step = inst.operand
            elif inst.opcode == Instruction.NOP:
                pass
            else:
                raise ValueError(
                    "invalid instruction={} pc={}".format(inst.opcode, pc))
            pc += pc_step
        if pc in visited:
            return False
        return True

    def monkeypatch(self, pc):
        # Change a program instruction at program counter pc
        # from JMP to NOP or from NOP to JMP
        inst = self.program[pc]
        if inst.opcode == Instruction.JMP:
            inst.opcode = Instruction.NOP
        elif inst.opcode == Instruction.NOP:
            inst.opcode = Instruction.JMP
        return None


def get_puzzle_input(filename="input.txt"):
    with open(filename, "r") as f:
        text = f.read()
    return text


def part1(sourcecode):
    prog = BootCode(sourcecode)
    prog.run()
    return prog.accumulator


def part2(sourcecode):
    prog = BootCode(sourcecode)

    # Find a line to monkeypatch
    for i in range(0, len(prog.program)):
        if prog.program[i].opcode in {Instruction.JMP, Instruction.NOP}:
            # Change JMP to NOP
            prog.monkeypatch(i)
            success = prog.run()
            if success:
                return prog.accumulator
            # Switch it back, we're not done yet
            prog.monkeypatch(i)

    raise ValueError("no monkeypatch resulted in success")


test_input = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""


def test():
    prog = BootCode(test_input)
    prog.run()
    return prog.accumulator


if __name__ == "__main__":
    source = get_puzzle_input("input.txt")
    print(part2(source))
