from inspect import signature
import logging
import sys

logging.basicConfig(stream=sys.stderr, level=logging.WARN)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return Point(self.x + other.x, self.y + other.y)

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.x == other.x and self.y == other.y


class Done(Exception):
    pass


# Needs to exist before the actual computer class for decorators
class IntcodeComputerMeta(type):
    op_codes = {}

    @classmethod
    def opcode(cls, n):
        def wrapper(func):
            assert n not in cls.op_codes
            cls.op_codes[n] = func
            params = signature(func).parameters
            func.n_args = len(params)
            func.needs_self = 'self' in params
            if func.needs_self:
                func.n_args -= 1
            func.name = func.__name__

            def wrapped(*args):
                return func(*args)
            return wrapped
        return wrapper


class IntcodeComputer(metaclass=IntcodeComputerMeta):
    def __init__(self, code):
        self.code = code
        self.pointer = 0
        self.input = []
        self.output = []
        self.done = False

    @property
    def func(self):
        return type(self).op_codes[self.code[self.pointer] % 100]

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
        result = func(*self.args)
        self.pointer += 1 + func.n_args
        if result is not None:
            assert isinstance(result, int)
            logging.debug(f"self.code[{self.code[self.pointer]}] = {result}")
            self.code[self.code[self.pointer]] = result
            self.pointer += 1

