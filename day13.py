"""Solution to day 13 of Advent of Code"""

import re
import itertools
import collections
import math
import logging
import sys

from get_input import get_input, line_parser
from common import Point, IntcodeComputerMeta, IntcodeComputer, Done

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


class IntcodeComputerDay13(IntcodeComputer):
    def __init__(self, code, *args, **kwargs):
        super().__init__(code, *args, **kwargs)
        self.relative_base = 0
        self.code = collections.defaultdict(int, enumerate(code))
        self.screen_x = 41
        self.screen_y = 25
        self.score = None
        self.clear_screen()
        self.ball = None
        self.paddle = None
        self.characters = {
            0: ' ',
            1: '|',
            2: '-',
            3: '_',
            4: 'o',
        }

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
        if self.ball.x == self.paddle.x:
            self.input.append(0)
        elif self.ball.x > self.paddle.x:
            self.input.append(1)
        elif self.ball.x < self.paddle.x:
            self.input.append(-1)
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

    def draw_screen(self):
        print('\n'.join(''.join(row) for row in self.screen))
        print(self.score)

    def clear_screen(self):
        self.screen = [
            [None for _ in range(self.screen_x)]
            for _ in range(self.screen_y)
        ]


def part1(code):
    computer = IntcodeComputerDay13(code)
    while True:
        try:
            computer.step()
        except Done:
            break
    total = 0
    for i in range(2, len(computer.output), 3):
        if computer.output[i] == 2:
            total += 1
    return total


def part2(code):
    code = code.copy()
    code[0] = 2
    computer = IntcodeComputerDay13(code)
    while True:
        if len(computer.output) == 3:
            x, y, value = computer.output
            computer.output.clear()
            if value == 3:
                computer.paddle = Point(x, y)
            if value == 4:
                computer.ball = Point(x, y)
            if x == -1 and y == 0:
                computer.score = value
                continue
            computer.screen[y][x] = computer.characters[value]
        try:
            computer.step()
        except Done:
            break
    return computer.score


if __name__ == '__main__':
    lines = line_parser(get_input(13, 2019), seperator=',')
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
