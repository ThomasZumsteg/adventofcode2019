"""Solution do day 2 of Advent of Code"""

from itertools import product
import inspect

from get_input import get_input, line_parser


class Done(Exception):
    pass


class Program:
    _opcodes = {}

    def __init__(self, program):
        self._program = program[:]
        self._pointer = 0

    @classmethod
    def run_until_complete(cls, program):
        this = cls(program)
        while True:
            try:
                this.step()
            except Done:
                return this

    def step(self):
        func = self._opcodes[self[self._pointer]]
        self._pointer += 1
        args = [self[self[a]] for a in
                range(self._pointer, self._pointer+func.n_args)]
        answer = func(*args)
        self._pointer += func.n_args
        self[self[self._pointer]] = answer
        self._pointer += 1

    def __getitem__(self, item):
        return self._program[item]

    def __setitem__(self, item, value):
        self._program[item] = value

    @classmethod
    def opcode(cls, code):
        def wrapper(func):
            def wrapped(*args):
                return func(*args)
            wrapped.n_args = len(inspect.getfullargspec(func).args)
            cls._opcodes[code] = wrapped
            return wrapped
        return wrapper


@Program.opcode(1)
def add(a, b):
    return a + b


@Program.opcode(2)
def mult(a, b):
    return a * b


@Program.opcode(99)
def done():
    raise Done("Program complete")


def part1(start):
    program = start[:]
    program[1:3] = [12, 2]
    return Program.run_until_complete(program)[0]


def part2(lines):
    for n, v in product(range(100), range(100)):
        program = lines[:]
        program[1:3] = [n, v]
        if Program.run_until_complete(program)[0] == 19690720:
            return n * 100 + v
    raise Exception("No solution found")


if __name__ == "__main__":
    TEST = [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]
    assert Program.run_until_complete(TEST)[0] == 3500

    LINES = line_parser(get_input(day=2, year=2019), seperator=',')
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
