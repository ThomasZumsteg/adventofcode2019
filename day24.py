"""Solution to day 24 of Advent of Code"""

import collections
import copy
import re

from get_input import get_input, line_parser
from common import Point


def part1(lines):
    state = copy.deepcopy(lines)
    seen = set()
    while True:
        new_state = state
        state = tuple(tuple(row) for row in state)
        if state in seen:
            break
        seen.add(state)
        len_state = len(state)
        len_row = len(state[0])
        for r, row in enumerate(state):
            for c, char in enumerate(row):
                bugs = 0
                for point in Point.directions:
                    try:
                        if 0 <= point.y+r < len_state and\
                                0 <= point.x+c < len_row and\
                                state[point.y+r][point.x+c] == '#':
                            bugs += 1
                    except IndexError:
                        pass
                if char == '#' and bugs != 1:
                    new_state[r][c] = '.'
                elif char == '.' and 1 <= bugs < 3:
                    new_state[r][c] = '#'
        state = new_state
    total = 0
    for n, char in enumerate(char for row in state for char in row):
        if char == '#':
            total += 2 ** n
    return total


def adjacent(pos):
    x, y, d = pos
    for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        if x + dx == 2 and y + dy == 2:
            if x == 1:
                for my in range(5):
                    yield (0, my, d+1)
            elif y == 1:
                for mx in range(5):
                    yield (mx, 0, d+1)
            elif x == 3:
                for my in range(5):
                    yield (4, my, d+1)
            elif y == 3:
                for mx in range(5):
                    yield (mx, 4, d+1)
        elif x + dx == -1:
            yield (1, 2, d-1)
        elif y + dy == -1:
            yield (2, 1, d-1)
        elif x + dx == 5:
            yield (3, 2, d-1)
        elif y + dy == 5:
            yield (2, 3, d-1)
        else:
            yield (x + dx, y + dy, d)


def part2(lines, minutes=200):
    state = {}
    for r, row in enumerate(lines):
        for c, char in enumerate(row):
            if char == '#':
                state[(c, r, 0)] = char
    for m in range(minutes):
        new_state = state.copy()
        positions = set(state.items())
        positions.update(
            (a, state.get(a, '.'))
            for p in state for a in adjacent(p))
        for pos, char in positions:
            bugs = 0
            for adj in adjacent(pos):
                if state.get(adj, '.') == '#':
                    bugs += 1
            if char == '#' and bugs != 1:
                del new_state[pos]
            elif char == '.' and 1 <= bugs < 3:
                new_state[pos] = '#'
        state = new_state
        # depths = [p[2] for p in state]
        # for d in range(min(depths), max(depths)+1):
        # if m == 0:
        #     for y in range(0, 5):
        #         for x in range(0, 5):
        #             if x == 2 and y == 2:
        #                 print('?', end='')
        #             else:
        #                 print(state.get((x, y, 0), '.'), end='')
        #         print()
        #     print()
    return len(state)


TEST1 = """
....#
#..#.
#..##
..#..
#....
"""


if __name__ == '__main__':
    assert part1(line_parser(TEST1.strip(), parse=list)) == 2129920
    lines = line_parser(get_input(24, 2019), parse=list)
    breakpoint()
    print(f"Part 1: {part1(lines)}")
    breakpoint()
    assert part2(line_parser(TEST1.strip(), parse=list), minutes=10) == 99
    # Between 1891 and 2009
    print(f"Part 2: {part2(lines)}")
