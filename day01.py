"""Solution do day 1 of Advent of Code"""

from get_input import get_input, line_parser

def part1(lines):
    total = 0
    for part in lines:
        total += (part // 3) - 2
    return total

def get_fuel(size):
    total = 0
    while True:
        size = (size // 3) - 2
        if size < 0:
            break
        total += size
    return total

def part2(lines):
    total = 0
    for line in lines:
        total += get_fuel(line)
    return total

if __name__ == "__main__":
    LINES = line_parser(get_input(day=1, year=2019)) 
    print(f"Part 1: {part1(LINES)}")
    assert get_fuel(14) == 2
    assert get_fuel(1969) == 966
    assert get_fuel(100756) == 50346
    print(f"Part 2: {part2(LINES)}")
