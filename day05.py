"""Solution to day 5 of Advent of Code"""

from get_input import get_input, line_parser
from common import IntcodeComputerMeta, IntcodeComputer, Done


class IntcodeComputerDay5(IntcodeComputer):
    @IntcodeComputerMeta.opcode(1)
    def add(a, b):
        return a + b

    @IntcodeComputerMeta.opcode(2)
    def mult(a, b):
        return a * b

    @IntcodeComputerMeta.opcode(3)
    def input(self):
        return self.input.pop(0)

    @IntcodeComputerMeta.opcode(4)
    def output(self, a):
        self.output.append(a)

    @IntcodeComputerMeta.opcode(5)
    def jump_if_true(self, a, b):
        if a != 0:
            self.pointer = b - 3

    @IntcodeComputerMeta.opcode(6)
    def jump_if_false(self, a, b):
        if a == 0:
            self.pointer = b - 3

    @IntcodeComputerMeta.opcode(7)
    def less_than(a, b):
        return int(a < b)

    @IntcodeComputerMeta.opcode(8)
    def equals(a, b):
        return int(a == b)

    @IntcodeComputerMeta.opcode(99)
    def done():
        raise Done


def part1(code):
    computer = IntcodeComputerDay5(code.copy())
    computer.input.append(1)
    try:
        while True:
            print(f"{computer.pointer} -> {computer.func.name}")
            computer.step()
    except Done:
        result = tuple(n for n in computer.output if n != 0)
        assert len(result) == 1
        return result[0]


def part2(code):
    computer = IntcodeComputerDay5(code.copy())
    computer.input.append(5)
    try:
        while True:
            computer.step()
    except Done:
        assert len(computer.output) == 1
        return computer.output[0]


if __name__ == '__main__':
    lines = line_parser(get_input(5, 2019), seperator=',')
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
