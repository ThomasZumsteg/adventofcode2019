"""Solution to day 25 of Advent of Code"""

import collections
import re

from get_input import get_input, line_parser
from common import (
        Done,
        IntcodeComputer,
        IntcodeComputerMeta,
        Point,
    )


class IntcodeComputerDay25(IntcodeComputer):
    def __init__(self, code, *args, **kwargs):
        super().__init__(code, *args, **kwargs)
        self.relative_base = 0
        self.code = collections.defaultdict(int, enumerate(code))
        self._idle = 0

    @property
    def idle(self):
        return len(self.input) == 0 and self._idle > 2

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
        if len(self.input) > 0:
            self._idle = 0
            return self.input.pop(0)
        self._idle += 1
        return -1

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


class Walker:
    def __init__(self):
        self.position = Point(0, 0)
        self.inv = []
        self.blacklist = set([])

    def read(self, text):
        if 'pressure plate' in text:
            return None




def part1(code):
    computer = IntcodeComputerDay25(code)
    while True:
        try:
            computer.step()
        except Done:
            break
        if computer.output and computer.output[-1] == ord('\n'):
            line = ''.join(chr(c) for c in computer.output)
            print(line, end='')
            if line == 'Command?\n':
                command = input()
                computer.input.extend(ord(c) for c in command + '\n')
            computer.output.clear()


if __name__ == '__main__':
    lines = line_parser(get_input(25, 2019), seperator=',')
    print(f"Part 1: {part1(lines)}")
