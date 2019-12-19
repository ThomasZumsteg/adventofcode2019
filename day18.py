"""Solution to day 18 of Advent of Code"""

import collections
import copy
import itertools
import re
import heapq

from common import Point
from get_input import get_input, line_parser


class State(collections.namedtuple("State", 'position seen keys steps')):
    def __lt__(self, other):
        return (self.steps * len(other.keys)) < (other.steps * len(self.keys))

    def __eq__(self, other):
        return self.steps == other.steps and len(self.keys) == len(other.keys)


def part1(inital):
    mapping = {}
    all_doors = {}
    all_keys = {}
    start = None
    for r, row in enumerate(inital):
        for c, char in enumerate(row):
            point = Point(c, r)
            if char.upper() != char.lower() or char == '@':
                if char == '@':
                    assert start is None
                    start = point
                elif char.upper() == char:
                    all_doors[point] = char
                elif char.lower() == char:
                    all_keys[point] = char
                else:
                    raise NotImplementedError
                char = '.'
            assert char in {'.', '#'}, "Not a valid map character"
            mapping[point] = char
    assert start is not None, "No start location found"
    distances = {(frozenset(), start): 0}
    for rnd in range(len(all_keys)):
        print(f"Round {rnd}/{len(all_keys)}")
        next_distances = {}
        for state, steps in distances.items():
            keys, pos = state
            seen = set()
            queue = [(pos, steps)]
            while queue:
                pos, steps = queue.pop(0)
                if pos in seen:
                    continue
                seen.add(pos)
                if mapping[pos] == '#' or (
                    pos in all_doors and
                    all_doors[pos].lower() not in keys
                ):
                    continue
                if pos in all_keys and all_keys[pos] not in keys:
                    found_keys = keys.union(all_keys[pos])
                    state = (found_keys, pos)
                    if state in next_distances:
                        steps = min(steps, next_distances[state])
                    next_distances[state] = steps
                    continue
                for move in Point.directions:
                    queue.append((pos+move, steps+1))
        distances = next_distances
    return min(distances.values())


def part2(inital):
    mapping = []
    all_doors = {}
    all_keys = {}
    start = None
    for r, chars in enumerate(inital):
        row = []
        for c, char in enumerate(chars):
            point = Point(c, r)
            if char.upper() != char.lower() or char == '@':
                if char == '@':
                    assert start is None
                    start = point
                elif char.upper() == char:
                    all_doors[point] = char
                elif char.lower() == char:
                    all_keys[point] = char
                else:
                    raise NotImplementedError
                char = '.'
            assert char in {'.', '#'}, "Not a valid map character"
            row.append(char)
        mapping.append(row)
    mapping = tuple(mapping)
    assert start is not None, "No start location found"
    starts = tuple(start+diff for diff in (
        Point(1, 1),
        Point(1, -1),
        Point(-1, 1),
        Point(-1, -1),
    ))
    for diff in Point.directions + (Point(0, 0),):
        mapping[start.y+diff.y][start.x+diff.x] = '#'
    mapping = tuple(tuple(row) for row in mapping)
    distances = {(frozenset(), starts): 0}
    for rnd in range(len(all_keys)):
        print(f"Round {rnd}/{len(all_keys)} -> {len(distances)}")
        next_distances = {}
        for state, state_steps in distances.items():
            keys, bots = state
            for b in range(len(bots)):
                seen = set()
                queue = [(bots[b], state_steps)]
                while queue:
                    pos, steps = queue.pop(0)
                    if pos in seen:
                        continue
                    seen.add(pos)
                    if mapping[pos.y][pos.x] == '#' or (
                        pos in all_doors and
                        all_doors[pos].lower() not in keys
                    ):
                        continue
                    if pos in all_keys and all_keys[pos] not in keys:
                        found_keys = keys.union(all_keys[pos])
                        new_bots = list(bots)
                        new_bots[b] = pos
                        state = (found_keys, tuple(new_bots))
                        if state in next_distances:
                            steps = min(steps, next_distances[state])
                        next_distances[state] = steps
                        continue
                    for move in Point.directions:
                        queue.append((pos+move, steps+1))
        distances = next_distances
    return min(distances.values())


TEST1 = """
#########
#b.A.@.a#
#########

"""

TEST2 = """
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################
"""

TEST3 = """
#############
#DcBa.#.GhKl#
#.###...#I###
#e#d#.@.#j#k#
###C#...###J#
#fEbA.#.FgHi#
#############
"""

if __name__ == '__main__':
    # assert part1(line_parser(TEST1.strip(), parse=list)) == 8
    # assert part1(line_parser(TEST2.strip(), parse=list)) == 86
    mapping = line_parser(get_input(18, 2019), parse=list)
    # print(f"Part 1: {part1(mapping)}")
    assert part2(line_parser(TEST3.strip(), parse=list)) == 32
    print(f"Part 2: {part2(mapping)}")
