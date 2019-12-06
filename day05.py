"""Solution to day 5 of Advent of Code"""

from collections import defaultdict

from get_input import get_input, line_parser

STDIN = []
STDOUT = []
POINTER = None


def add(a, b):
    return a + b


def mult(a, b):
    return a * b


def store():
    return STDIN.pop(0)


def output(a):
    STDOUT.append(a)


def jump_if_true(a, b):
    if a != 0:
        global POINTER
        POINTER = b
        return True
    return False


def jump_if_false(a, b):
    if a == 0:
        global POINTER
        POINTER = b
        return True
    return False


def less_than(a, b):
    return int(a < b)


def equal(a, b):
    return int(a == b)


class Done(Exception):
    pass


def exit():
    raise Done


OPCODES = {
    1: (add, 2),
    2: (mult, 2),
    3: (store, 0),
    4: (output, 1),
    5: (jump_if_true, 2),
    6: (jump_if_false, 2),
    7: (less_than, 2),
    8: (equal, 2),
    99: (exit, 0),
}


def part1(code):
    code = list(code)
    global POINTER
    POINTER = 0
    STDIN.clear()
    STDIN.append(1)
    STDOUT.clear()
    while True:
        opcode = code[POINTER]
        func, n_args = OPCODES[opcode % 100]
        args = []
        for n in range(n_args):
            mode = (opcode // 10**(n+2)) % 10
            arg = code[POINTER+1+n]
            if mode == 0:
                assert arg >= 0
                arg = code[arg]
            args.append(arg)
        try:
            result = func(*args)
        except Done:
            break
        if opcode % 100 in {5, 6}:
            if result:
                continue
        else:
            if result is not None:
                n_args += 1
                code[code[POINTER+n_args]] = result
        POINTER += n_args + 1
    result = tuple(n for n in STDOUT if n != 0)
    assert len(result) == 1
    return result[0]


def part2(code):
    code = list(code)
    global POINTER
    POINTER = 0
    STDIN.clear()
    STDIN.append(5)
    STDOUT.clear()
    while True:
        opcode = code[POINTER]
        func, n_args = OPCODES[opcode % 100]
        args = []
        for n in range(n_args):
            mode = (opcode // 10**(n+2)) % 10
            arg = code[POINTER+1+n]
            if mode == 0:
                assert arg >= 0
                arg = code[arg]
            args.append(arg)
        try:
            result = func(*args)
        except Done:
            break
        if opcode % 100 in {5, 6}:
            if result:
                continue
        else:
            if result is not None:
                n_args += 1
                code[code[POINTER+n_args]] = result
        POINTER += n_args + 1
    assert len(STDOUT) == 1
    return STDOUT[0]


if __name__ == '__main__':
    lines = line_parser(get_input(5, 2019), seperator=',')
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
