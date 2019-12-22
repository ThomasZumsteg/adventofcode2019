"""Solution to day 21 of Advent of Code"""

import collections
import copy
import itertools
import re

from get_input import get_input, line_parser
from common import (
        Done,
        IntcodeComputer,
        IntcodeComputerMeta,
        Point,
    )


class IntcodeComputerDay21(IntcodeComputer):
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
        func = self.func
        # import pdb; pdb.set_trace()
        result = func(*self.args)
        if result is not None:
            assert isinstance(result, int)
            pos = self.code[self.pointer+1+func.n_args]
            if self.code[self.pointer] // 10**(2+self.func.n_args) == 2:
                pos += self.relative_base
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
    computer = IntcodeComputerDay21(code.copy())
    instructions = [
        "NOT J J",
        "AND A J",
        "AND B J",
        "AND C J",
        "NOT J J",
        "NOT D T",
        "NOT T T",
        "AND T J",
        "WALK",
    ]
    assert len(instructions) < 15
    while True:
        computer.step()
        message = ''.join(chr(o) for o in computer.output)
        if message == 'Input instructions:\n':
            print(message, end='')
            computer.input.extend(
                ord(char) for char in '\n'.join(instructions) + '\n'
            )
            computer.output.clear()
            break
    while True:
        computer.step()
        if len(computer.output) > 0:
            char = computer.output.pop()
            try:
                print(chr(char), end='')
            except ValueError:
                return char


def part2(code):
    computer = IntcodeComputerDay21(code.copy())
    instructions = [
        'OR A T',
        'AND B T',
        'AND C T',
        'NOT T J',
        'AND D J',
        'NOT E T',
        'NOT T T',
        'OR H T',
        'AND T J',
        'RUN',
    ]
    assert len(instructions) < 15
    while True:
        computer.step()
        message = ''.join(chr(o) for o in computer.output)
        if message == 'Input instructions:\n':
            print(message, end='')
            computer.input.extend(
                ord(char) for char in '\n'.join(instructions) + '\n'
            )
            computer.output.clear()
            break
    while True:
        computer.step()
        if len(computer.output) > 0:
            char = computer.output.pop()
            try:
                print(chr(char), end='')
            except ValueError:
                return char


if __name__ == '__main__':
    lines = line_parser(get_input(21, 2019), seperator=',')
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
