"""Solution to day 9 of Advent of Code"""

import collections
import logging
import sys

from get_input import get_input, line_parser
from common import IntcodeComputer, IntcodeComputerMeta, Done


logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


class IntcodeComputerDay9(IntcodeComputer):
    def __init__(self, code, *args, **kwargs):
        super().__init__(code, *args, **kwargs)
        self.relative_base = 0
        self.code = collections.defaultdict(int, enumerate(code))

    @property
    def args(self):
        args = []
        if self.func.needs_self:
            args.append(self)
        for n in range(self.func.n_args):
            mode = (self.code[self.pointer] // 10**(n+2)) % 10
            arg = self.code[self.pointer+1+n]
            if mode == 0:
                assert arg >= 0
                arg = self.code[arg]
            elif mode == 2:
                assert self.relative_base+arg >= 0
                arg = self.code[self.relative_base+arg]
            args.append(arg)
        return args

    def step(self):
        logging.debug(
            f"Calling {self.pointer} -> {self.func.name}(" +
            ', '.join(
                str(a) if isinstance(a, int) else 'self' for a in self.args
            ) +
            ")"
        )
        func = self.func
        # import pdb; pdb.set_trace()
        result = func(*self.args)
        if result is not None:
            assert isinstance(result, int)
            pos = self.code[self.pointer+1+func.n_args]
            if self.code[self.pointer] // 10**(2+self.func.n_args) == 2:
                pos += self.relative_base
            logging.debug(f"self.code[{pos}] = {result}")
            assert pos >= 0
            self.code[pos] = result
            self.pointer += 1
        self.pointer += 1 + func.n_args

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

    @IntcodeComputerMeta.opcode(9)
    def relative_base_offset(self, a):
        self.relative_base += a

    @IntcodeComputerMeta.opcode(99)
    def done(self):
        self.done = True
        raise Done


def part1(code):
    computer = IntcodeComputerDay9(code.copy())
    computer.input.append(1)
    try:
        while True:
            computer.step()
    except Done:
        assert len(computer.output) == 1
        return computer.output.pop()


def part2(code):
    computer = IntcodeComputerDay9(code.copy())
    computer.input.append(2)
    try:
        while True:
            computer.step()
    except Done:
        assert len(computer.output) == 1
        return computer.output.pop()


def test_day9_part1_1():
    code = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100,
            16, 101, 1006, 101, 0, 99]
    computer = IntcodeComputerDay9(code.copy())
    try:
        while True:
            computer.step()
    except Done:
        assert computer.output == code


def test_day9_part1_2():
    code = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
    computer = IntcodeComputerDay9(code.copy())
    try:
        while True:
            computer.step()
    except Done:
        assert len(str(computer.output[0])) == 16


if __name__ == '__main__':
    # test_day9_part1_1()
    # test_day9_part1_2()
    lines = line_parser(get_input(9, 2019), seperator=',')
    # Not 203
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
