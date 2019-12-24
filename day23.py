"""Solution to day 23 of Advent of Code"""

import collections
import re

from get_input import get_input, line_parser
from common import (
        Done,
        IntcodeComputer,
        IntcodeComputerMeta,
        Point,
    )


class IntcodeComputerDay23(IntcodeComputer):
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


def part1(code):
    computers = {}
    for i in range(50):
        computers[i] = IntcodeComputerDay23(code)
        computers[i].input.append(i)
    while True:
        for i, computer in computers.items():
            computer.step()
            if len(computer.output) >= 3:
                dst = computer.output.pop(0)
                x = computer.output.pop(0)
                y = computer.output.pop(0)
                if dst == 255:
                    return y
                computers[dst].input.append(x)
                computers[dst].input.append(y)
    raise NotImplementedError


def part2(code):
    computers = {}
    nat = None
    y_last = None
    for i in range(50):
        computers[i] = IntcodeComputerDay23(code)
        computers[i].input.append(i)
    while True:
        for src, computer in computers.items():
            computer.step()
            if len(computer.output) >= 3:
                dst = computer.output.pop(0)
                x = computer.output.pop(0)
                y = computer.output.pop(0)
                # print(f"{src} -> {dst}: ({x}, {y})")
                if dst == 255:
                    nat = (x, y)
                else:
                    computers[dst].input.append(x)
                    computers[dst].input.append(y)
        for c, computer in computers.items():
            if not computer.idle:
                break
        else:
            if y_last == nat[1]:
                return y_last
            y_last = nat[1]
            computers[0].input.append(nat[0])
            computers[0].input.append(nat[1])
    raise NotImplementedError


if __name__ == '__main__':
    lines = line_parser(get_input(23, 2019), seperator=',')

    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
