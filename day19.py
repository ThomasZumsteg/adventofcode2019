"""Solution to day 19 of Advent of Code"""

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


class IntcodeComputerDay19(IntcodeComputer):
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


def from_intcomputer(code, point):
    computer = IntcodeComputerDay19(code.copy())
    computer.input.append(point.x)
    computer.input.append(point.y)
    while len(computer.output) <= 0:
        computer.step()
    return computer.output[0]


def print_space(code, upper, get_point=from_intcomputer, size=100):
    print(f"\nDrawing {upper} - {size}")
    for y in range(upper.y, upper.y+size):
        for x in range(upper.x, upper.x+size):
            if get_point(code, Point(x, y)) == 1:
                print('#', end='')
            else:
                print('.', end='')
        print()


def part1(code):
    total = 0
    # print_space(code, Point(0, 0), size=50)
    for y, x in itertools.product(range(50), range(50)):
        total += from_intcomputer(code, Point(x, y))
    return total


def part2(code, get_point=from_intcomputer, size=100):
    size -= 1
    upper = Point(size, 0)
    while True:
        while get_point(code, upper) == 0:
            upper += Point(0, 1)
        if get_point(code, upper+Point(-size, size)) == 1:
            break
        upper += Point(1, 0)
    return (upper.x - size) * 10000 + upper.y


TEST1 = """
#.......................................
.#......................................
..##....................................
...###..................................
....###.................................
.....####...............................
......#####.............................
......######............................
.......#######..........................
........########........................
.........#########......................
..........#########.....................
...........##########...................
...........############.................
............############................
.............#############..............
..............##############............
...............###############..........
................###############.........
................#################.......
.................########OOOOOOOOOO.....
..................#######OOOOOOOOOO#....
...................######OOOOOOOOOO###..
....................#####OOOOOOOOOO#####
.....................####OOOOOOOOOO#####
.....................####OOOOOOOOOO#####
......................###OOOOOOOOOO#####
.......................##OOOOOOOOOO#####
........................#OOOOOOOOOO#####
.........................OOOOOOOOOO#####
..........................##############
..........................##############
...........................#############
............................############
.............................###########
"""


def from_test(_, point):
    return int(TEST1.strip().splitlines()[point.y][point.x] != '.')


if __name__ == '__main__':
    lines = line_parser(get_input(19, 2019), seperator=',')
    print(f"Part 1: {part1(lines)}")
    assert part2(lines, get_point=from_test, size=10) == 250020
    print(f"Part 2: {part2(lines)}")
