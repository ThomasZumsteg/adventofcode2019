"""Solution do day 2 of Advent of Code"""

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

    def __init__(self, name, path, start=Point(0, 0)):
        self._path = defaultdict(set)
        self.name = name
        step = 0
        location = start
        for direction, n_steps in path:
            for _ in range(n_steps):
                step += 1
                location += Wire.HEADINGS[direction]
                self._path[location].add(step)

    def intersections(self, other):
        intersections = {}
        for point, self_value in self._path.items():
            other_value = other._path[point]
            if self_value and other_value:
                intersections[point] = {
                    self.name: self_value,
                    other.name: other_value
                }
        return intersections


def part1(wires):
    wire_paths = [Wire(n, path) for n, path in enumerate(wires)]
    intersections = wire_paths[0].intersections(wire_paths[1])
    return min(abs(point.x) + abs(point.y) for point in intersections)


def part2(wires):
    wire_paths = [Wire(n, path) for n, path in enumerate(wires)]
    intersections = wire_paths[0].intersections(wire_paths[1])

    def key(values):
        path1_min = min(values[wire_paths[0].name])
        path2_min = min(values[wire_paths[1].name])
        return path1_min + path2_min

    first = min(intersections.values(), key=key)
    return min(v for value in first.values() for v in value)


def parse(line):
    return tuple((e[0], int(e[1:])) for e in line.split(','))


if __name__ == "__main__":
    TEST1 = """R8,U5,L5,D3\nU7,R6,D4,L4"""
    assert part1(line_parser(TEST1, parse=parse)) == 6
    TEST2 = """R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83"""
    assert part1(line_parser(TEST2, parse=parse)) == 159
    values = line_parser(get_input(day=3, year=2019), parse=parse)
    print(f"Part 1: {part1(values)}")
    print(f"Part 2: {part2(values)}")
