"""Solution to day 7 of Advent of Code"""
import itertools
import logging
import sys

from get_input import get_input, line_parser
from common import IntcodeComputerMeta, IntcodeComputer, Done

logging.basicConfig(stream=sys.stderr, level=logging.WARN)


class IntcodeComputerDay7(IntcodeComputer):
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
    def done(self):
        self.done = True
        raise Done


def part1(code, n_computers=5):
    max_output = 0
    for combo in itertools.permutations(range(n_computers)):
        computers = []
        for n in combo:
            computer = IntcodeComputerDay7(code.copy())
            computer.input.append(n)
            computers.append(computer)
        output = 0
        for comp in computers:
            comp.input.append(output)
            while not comp.output:
                comp.step()
            output = comp.output.pop()
            logging.info(f"Passing {output}")
        max_output = max(max_output, output)
    return max_output


def part2(code, n_computers=5):
    max_output = 0
    for combo in itertools.permutations(range(5, 10)):
        computers = []
        for n in combo:
            computer = IntcodeComputerDay7(code.copy())
            computer.input.append(n)
            computers.append(computer)
        output = 0
        try:
            while True:
                for comp in computers:
                    comp.input.append(output)
                    while not comp.output:
                        comp.step()
                    output = comp.output.pop()
                    logging.info(f"Passing {output}")
                last_output = output
        except Done:
            max_output = max(max_output, last_output)
    return max_output


if __name__ == '__main__':
    assert part1(
        [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]
    ) == 43210
    lines = line_parser(get_input(7, 2019), seperator=',')
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
