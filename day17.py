"""Solution to day 17 of Advent of Code"""

import collections
import itertools
import re

from common import Done, IntcodeComputer, IntcodeComputerMeta, Point
from get_input import get_input, line_parser


class IntcodeComputerDay17(IntcodeComputer):
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

    def draw_screen(self):
        print('\n'.join(''.join(row) for row in self.screen))
        print(self.score)

    def clear_screen(self):
        self.screen = [
            [None for _ in range(self.screen_x)]
            for _ in range(self.screen_y)
        ]


def print_scaffold(mapping):
    xs = [p.x for p in mapping.keys()]
    ys = [p.y for p in mapping.keys()]
    result = ''
    for y in range(min(ys), max(ys)+1):
        for x in range(min(xs), max(xs)+1):
            result += mapping[Point(x, y)]
        result += '\n'
    print(result)


def part1(code):
    computer = IntcodeComputerDay17(code)
    while True:
        try:
            computer.step()
        except Done:
            break
    scaffold_map = collections.defaultdict(lambda: '.')
    point = Point(0, 0)
    for char in computer.output:
        if char == ord('\n'):
            point = Point(0, point.y+1)
        else:
            scaffold_map[point] = chr(char)
            point += Point(1, 0)
    directions = (Point(0, 1), Point(0, -1), Point(1, 0), Point(-1, 0))
    total = 0
    scaffold = set(key for key, value in scaffold_map.items() if value != '.')
    for point in scaffold:
        if all(point + d in scaffold for d in directions):
            total += point.x * point.y
    return total


def part2(code):
    computer = IntcodeComputerDay17(code.copy())
    while True:
        try:
            computer.step()
        except Done:
            break
    scaffold_map = collections.defaultdict(lambda: '.')
    point = Point(0, 0)
    for char in computer.output:
        if char == ord('\n'):
            point = Point(0, point.y+1)
        else:
            scaffold_map[point] = chr(char)
            point += Point(1, 0)
    robots = [
        (p, v) for p, v in scaffold_map.items()
        if v in {'v', '^', '>', '<'}
    ]
    assert len(robots) == 1
    point, char = robots.pop()
    heading = {
        'v': Point(0, 1),
        '^': Point(0, -1),
        '<': Point(-1, 0),
        '>': Point(1, 0),
    }[char]
    directions = []
    while True:
        if scaffold_map[point + heading] != '#':
            if scaffold_map[point + heading.turn_left()] == '#':
                directions.append('L')
                heading = heading.turn_left()
            elif scaffold_map[point + heading.turn_right()] == '#':
                directions.append('R')
                heading = heading.turn_right()
            else:
                break
            directions.append(0)
        else:
            directions[-1] += 1
            point += heading

    # Compress directions via visual inspection
    program = 'A,B,A,C,A,B,A,C,B,C\nR,4,L,12,L,8,R,4\nL,8,R,10,R,10,R,6\nR,4,R,10,L,12\n'
    runner_code = code.copy()
    assert runner_code[0] == 1
    runner_code[0] = 2
    runner = IntcodeComputerDay17(runner_code.copy())
    # No video feed
    program += 'n\n'
    runner.input = [ord(c) for c in program + 'n\n']
    while True:
        try:
            runner.step()
        except Done:
            break
    return runner.output.pop()


if __name__ == '__main__':
    lines = line_parser(get_input(17, 2019), seperator=',')
    # not 3111
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
