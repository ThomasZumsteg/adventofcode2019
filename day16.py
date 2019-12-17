"""Solution to day 16 of Advent of Code"""

import functools

from get_input import get_input


class FFT:
    def __init__(self, pattern):
        self.pattern = pattern
        self.cache = {}

    @functools.lru_cache(maxsize=None)
    def get_digit(self, n, phase):
        if phase == 0:
            return self.pattern[n]
        total = 0
        for d in range(n, len(self.pattern)):
            case = ((d+1) - (n+1)) // (n+1)
            if case % 4 == 0:
                total += self.get_digit(d, phase-1)
            elif case % 4 == 2:
                total -= self.get_digit(d, phase-1)
        return abs(total) % 10


def part1(pattern, phases=100):
    fft = FFT(pattern)
    return ''.join(str(fft.get_digit(n, phases)) for n in range(8))


def part2(pattern, phases=100):
    digits = list(pattern * 10000)
    offset = int(''.join(str(d) for d in pattern[:7]))
    assert 2 * offset > len(digits), "Simplifying assumpting " +\
        "only works in the later half of the pattern"
    for phase in range(phases):
        total = sum(digits[offset:])
        for d, digit in enumerate(digits[offset:], offset):
            digits[d] = total % 10
            total -= digit
        assert total == 0
    return ''.join(str(d) for d in digits[offset:offset+8])


def parse(line):
    return tuple(int(d) for d in list(line.strip()))


if __name__ == '__main__':
    assert part1(parse('12345678'), phases=4) == '01029498'
    assert part1(parse('80871224585914546619083218645595')) == '24176176'
    lines = parse(get_input(16, 2019))
    print(f"Part 1: {part1(lines)}")
    assert part2(parse('03036732577212944063491565474664')) == '84462026'
    print(f"Part 2: {part2(lines)}")
