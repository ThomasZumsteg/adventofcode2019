"""Solution do day 3 of Advent of Code"""

from collections import defaultdict

from get_input import get_input, line_parser
from common import Point


class Wire:
    HEADINGS = {
        "U": Point(0, 1),
        "D": Point(0, -1),
        "R": Point(1, 0),
        "L": Point(-1, 0),
    }

    def __init__(self, path, start=Point(0, 0)):
        self._path = defaultdict(set)
        step = 0
        location = start
        for direction, n_steps in path:
            for _ in range(n_steps):
                step += 1
                location += Wire.HEADINGS[direction]
                self._path[location].add(step)

    def intersections(self, other):
        return set(p for p in self._path if p in other._path)


def part1(wires):
    wire_paths = [Wire(path) for n, path in enumerate(wires)]
    intersections = wire_paths[0].intersections(wire_paths[1])
    return min(abs(point.x) + abs(point.y) for point in intersections)


def part2(wires):
    wire_paths = [Wire(path) for n, path in enumerate(wires)]
    intersections = wire_paths[0].intersections(wire_paths[1])
    return min(
        min(wire_paths[0]._path[i]) + min(wire_paths[1]._path[i])
        for i in intersections
    )


def parse(line):
    return tuple((e[0], int(e[1:])) for e in line.split(','))


TEST1 = """R8,U5,L5,D3\nU7,R6,D4,L4"""
TEST2 = """R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83"""

if __name__ == "__main__":
    assert part1(line_parser(TEST1, parse=parse)) == 6
    assert part1(line_parser(TEST2, parse=parse)) == 159
    values = line_parser(get_input(day=3, year=2019), parse=parse)
    print(f"Part 1: {part1(values)}")
    assert part2(line_parser(TEST2, parse=parse)) == 610
    print(f"Part 2: {part2(values)}")
