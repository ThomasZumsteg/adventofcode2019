"""Solution to day 6 of Advent of Code"""

from collections import defaultdict

from get_input import get_input, line_parser


def part1(orbits):
    orbit_map = {b: a for a, b in orbits}
    orbit_count = 0
    for orbiter in orbit_map.keys():
        while orbiter in orbit_map:
            orbiter = orbit_map[orbiter]
            orbit_count += 1
    return orbit_count


def part2(orbits):
    orbit_map = defaultdict(set)
    for a, b in orbits:
        orbit_map[a].add(b)
        orbit_map[b].add(a)
    goal = list(orbit_map['SAN'])[0]
    start = list(orbit_map['YOU'])[0]
    queue = [(0, start)]
    seen = set()
    while queue:
        steps, current = queue.pop(0)
        if current == goal:
            return steps
        if current in seen:
            continue
        seen.add(current)
        for step in orbit_map[current]:
            queue.append((steps+1, step))
    raise Exception("Cannot be done")


def parse(line):
    a, b = line.split(')')
    return (a, b)


TEST1 = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L"""


if __name__ == '__main__':
    assert part1(line_parser(TEST1.strip(), parse=parse)) == 42
    lines = line_parser(get_input(6, 2019), parse=parse)
    print(f"Part 1: {part1(lines)}")
    test2 = line_parser(TEST1.strip(), parse=parse)
    test2.append(("K", "YOU"))
    test2.append(("I", "SAN"))
    assert part2(test2) == 4
    print(f"Part 2: {part2(lines)}")
