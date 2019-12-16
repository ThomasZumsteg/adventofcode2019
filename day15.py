"""Solution to day 15 of Advent of Code"""

import collections
import copy


from common import Done, IntcodeComputer, IntcodeComputerMeta, Point
from get_input import get_input, line_parser


class IntcodeComputerDay15(IntcodeComputer):
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


class Droid:
    directions = {
        1: Point(0, 1),
        2: Point(0, -1),
        3: Point(1, 0),
        4: Point(-1, 0),
    }

    def __init__(self, code):
        self.computer = IntcodeComputerDay15(code)
        self.position = Point(0, 0)
        self.steps = 0
        self.status = None

    def move(self, direction):
        self.computer.input.append(direction)
        self.steps += 1
        while len(self.computer.output) <= 0:
            self.computer.step()
        self.status = self.computer.output.pop()
        if self.status == 0:
            return
        self.position += self.directions[direction]


def part1(code):
    droids = [Droid(code.copy())]
    seen = set()

    while droids:
        droid = droids.pop(0)
        if droid.status == 2:
            return droid.steps
        if droid.position in seen:
            continue
        seen.add(droid.position)
        for direction in [1, 2, 3, 4]:
            new_droid = copy.deepcopy(droid)
            try:
                new_droid.move(direction)
            except Done:
                continue
            if droid.status == 0:
                print("\twall!")
            else:
                droids.append(new_droid)
    raise Exception("No solution found")


def part2(code):
    droids = [Droid(code.copy())]
    floor_map = {}
    leak = None

    while droids:
        droid = droids.pop(0)
        for direction in [1, 2, 3, 4]:
            new_droid = copy.deepcopy(droid)
            try:
                new_droid.move(direction)
            except Done:
                continue
            if new_droid.status == 0:
                check_point = new_droid.position +\
                    new_droid.directions[direction]
                assert check_point not in floor_map or\
                    floor_map[check_point] == '#'
                floor_map[check_point] = '#'
            if new_droid.position in floor_map:
                continue
            floor_map[new_droid.position] = '.'
            droids.append(new_droid)
            if new_droid.status == 2:
                leak = new_droid.position
    front = {leak}
    steps = 0
    while len(front) > 0:
        new_front = set()
        for point in front:
            if floor_map[point] in {'#', 'O'}:
                continue
            floor_map[point] = 'O'
            for direction in [
                    Point(0, 1), Point(0, -1),
                    Point(1, 0), Point(-1, 0)]:
                new_front.add(point + direction)
        front = new_front
        steps += 1
    assert all(value != '.' for value in floor_map.values())
    return steps - 2


if __name__ == '__main__':
    lines = line_parser(get_input(15, 2019), seperator=',')
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
