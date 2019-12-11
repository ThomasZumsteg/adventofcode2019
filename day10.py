"""Solution to day 10 of Advent of Code"""

import collections
import sys
import re
import math

from common import Point
from get_input import get_input, line_parser


def closest(asteriod_map, location, check):
    if location == check:
        return location
    diff = location - check
    step_size = math.gcd(diff.x, diff.y)
    step = Point(-diff.x / step_size, -diff.y / step_size)
    # print(f"{location} + {check} = {diff}")
    position = location + step
    while position != check:
        # print("\t" + f"Checking {position}")
        if asteriod_map[position] == '#':
            return position
        assert float(position.x).is_integer() and\
            float(position.y).is_integer()
        position += step
    return check


def part1(asteriod_map):
    best_detected = None
    for location, char in asteriod_map.items():
        if char != '#':
            continue
        detected = 0
        for check in asteriod_map.keys():
            if check != location and\
                    asteriod_map[check] == '#' and\
                    closest(asteriod_map, location, check) == check:
                detected += 1
        best_detected = best_detected or detected
        if detected > best_detected:
            best_detected = detected
    return best_detected


def order(firing_location, asteriod_map):
    order = collections.defaultdict(list)
    for point, char in asteriod_map.items():
        if char != '#':
            continue
        angle = (360 - firing_location.angle(
            firing_location + Point(0, -1),
            point
        )) % 360
        order[angle].append(point)
        order[angle].sort(
            key=lambda p: p.distance(firing_location),
            reverse=True
        )
    while any(len(v) > 0 for v in order.values()):
        for angle, targets in sorted(order.items(), key=lambda kv: kv[0]):
            if not targets:
                continue
            yield angle, targets.pop()


def part2(asteriod_map):
    best_detected = None
    best_location = None
    for location, char in asteriod_map.items():
        if char != '#':
            continue
        detected = 0
        for check in asteriod_map.keys():
            if check != location and\
                    asteriod_map[check] == '#' and\
                    closest(asteriod_map, location, check) == check:
                detected += 1
        best_detected = best_detected or detected
        if detected > best_detected:
            best_detected = detected
            best_location = location
    for n, (angle, point) in enumerate(order(best_location, asteriod_map), 1):
        if n == 200:
            return 100 * point.x + point.y
    raise Exception("Not enough asteroids")


def parse(text):
    asteroid_map = {}
    for y, row in enumerate(text.split('\n')):
        for x, char in enumerate(list(row)):
            asteroid_map[Point(x, y)] = char
    return asteroid_map


TEST1 = """.#..#
.....
#####
....#
...##"""


TEST2 = """.#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....X...###..
..#.#.....#....##"""

if __name__ == '__main__':
    assert 8 == part1(parse(TEST1))
    asteriod_map = parse(get_input(10, 2019))
    print(f"Part 1: {part1(asteriod_map)}")
    print(f"Part 2: {part2(asteriod_map)}")
