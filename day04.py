"""Solution do day 4 of Advent of Code"""

from collections import Counter

from get_input import line_parser, get_input


def has_doubles(digits):
    for a, b in zip(digits[1:], digits):
        if a == b:
            return True
    return False


def exactly_one_pair(digits):
    if digits[0] == digits[1] != digits[2]:
        return True
    if digits[0] != digits[1] == digits[2] != digits[3]:
        return True
    if digits[1] != digits[2] == digits[3] != digits[4]:
        return True
    if digits[2] != digits[3] == digits[4] != digits[5]:
        return True
    if digits[3] != digits[4] == digits[5]:
        return True
    return False


def inc_digits(digits):
    number = int(''.join(str(d) for d in digits))
    number += 1
    new_digits = [int(d) for d in list(str(number))]
    result = [new_digits[0]]
    for d in new_digits[1:]:
        result.append(max(result[-1], d))
    return result


def part1(lines):
    start, end = lines
    digits = [int(d) for d in list(str(start))]
    count = 0
    while int(''.join(str(d) for d in digits)) < end:
        if has_doubles(digits):
            count += 1
        digits = inc_digits(digits)
    return count


def part2(lines):
    start, end = lines
    digits = [int(d) for d in list(str(start))]
    count = 0
    while int(''.join(str(d) for d in digits)) < end:
        if exactly_one_pair(digits):
            print(''.join(str(d) for d in digits))
            count += 1
        digits = inc_digits(digits)
    return count


def parse(line):
    pass


if __name__ == "__main__":
    values = line_parser(get_input(day=4, year=2019), seperator='-')
    print(f"Part 1: {part1(values)}")
    print(f"Part 2: {part2(values)}")
