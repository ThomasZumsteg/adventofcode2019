"""Solution to day 22 of Advent of Code"""

from dataclasses import dataclass
import collections
import re

from get_input import get_input, line_parser


@dataclass
class Cut:
    N: int

    def __call__(self, deck):
        deck.rotate(-self.N)
        return deck

    def build(self, size, offset, increment):
        return (
            (offset + increment * self.N) % size,
            increment
        )


@dataclass
class Deal:
    N: int

    def __call__(self, deck):
        new_deck = deck.copy()
        cards = len(deck)
        index = 0
        for element in deck:
            new_deck[index] = element
            index = (index + self.N) % cards
        assert len(set(new_deck)) == len(deck)
        return new_deck

    def build(self, size, offset, increment):
        return (
            offset,
            increment * pow(self.N, size-2, size)
        )


@dataclass
class NewStack:
    def __call__(self, deck):
        deck.reverse()
        return deck

    def build(self, size, offset, increment):
        return (
            offset - increment,
            -increment,
        )


def parse(line):
    m = re.match(r'cut (-?\d+)', line)
    if m:
        return Cut(int(m.group(1)))
    m = re.match(r'deal with increment (\d+)', line)
    if m:
        return Deal(int(m.group(1)))
    m = re.match(r'deal into new stack', line)
    if m:
        return NewStack()
    raise NotImplementedError


def part1(steps, size=10007, find=2019):
    # deck = collections.deque(range(size))
    # for step in steps:
    #     deck = step(deck)
    # return deck.index(find)
    (offset, increment) = (0, 1)
    for step in steps:
        offset, increment = step.build(size, offset, increment)
    for n in range(size):
        if (offset + increment * n) % size == find:
            return n
    raise Exception("No Solution found")


def part2(steps,
          size=119315717514047,
          times=101741582076661,
          find=2020):
    (offset, increment) = (0, 1)
    for step in steps:
        offset, increment = step.build(size, offset, increment)
    final_increment = pow(increment, times, size)
    offset = offset * (1 - final_increment)\
        * pow((1-increment) % size, size-2, size)
    return (offset + final_increment * find) % size


TEST1 = """
deal with increment 7
deal into new stack
deal into new stack
"""

TEST2 = """
cut 6
deal with increment 7
deal into new stack
"""

if __name__ == "__main__":
    lines = line_parser(get_input(22, 2019), parse=parse)
    print(f"Part 1: {part1(lines)}")
    result = part1(lines)
    assert part2(lines, size=10007, times=1, find=result) == 2019

    result = part1(10 * lines)
    assert part2(lines, size=10007, times=10, find=result) == 2019
    # NOT: 39709994149318, 4671129802281
    print(f"Part 2: {part2(lines)}")
