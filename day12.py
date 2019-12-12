"""Solution to day 12 of Advent of Code"""

import re
import itertools
import collections
import math

from get_input import get_input, line_parser


class Point3d:
    def __init__(self, x, y, z):
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)

    def __add__(self, other):
        if not isinstance(other, Point3d):
            return NotImplemented
        return Point3d(self.x+other.x, self.y+other.y, self.z+other.z)

    def __eq__(self, other):
        if not isinstance(other, Point3d):
            return NotImplemented
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __repr__(self):
        return f"<x={self.x:3d}, y={self.y:3d}, z={self.z:3d}>"

    def abs(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def __hash__(self):
        return hash(hash(self.x) + hash(self.y) + hash(self.z))


class Moon:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def step(self):
        self.position += self.velocity

    def apply_gravity(self, other):
        for axis in ('x', 'y', 'z'):
            self_value = getattr(self.position, axis)
            other_value = getattr(other.position, axis)
            if self_value > other_value:
                setattr(self.velocity, axis, getattr(self.velocity, axis)-1)
                setattr(other.velocity, axis, getattr(other.velocity, axis)+1)
            elif self_value < other_value:
                setattr(self.velocity, axis, getattr(self.velocity, axis)+1)
                setattr(other.velocity, axis, getattr(other.velocity, axis)-1)

    @property
    def potential_energy(self):
        return self.position.abs()

    @property
    def kinetic_energy(self):
        return self.velocity.abs()

    def __repr__(self):
        return f"Moon(pos={self.position}, vel={self.velocity})"

    def __hash__(self):
        return hash(hash(self.position) + hash(self.velocity))

    def __eq__(self, other):
        if not isinstance(other, Moon):
            return NotImplemented
        return self.velocity == other.velocity and\
            self.position == other.position


def part1(positions, steps=1000):
    moons = [Moon(position, Point3d(0, 0, 0)) for position in positions]
    for n in range(steps):
        for moon_a, moon_b in itertools.combinations(moons, 2):
            moon_a.apply_gravity(moon_b)
        for moon in moons:
            moon.step()
    return sum(m.potential_energy * m.kinetic_energy for m in moons)


class PeriodTracker:
    def __init__(self):
        self.length = None
        self.first = None
        self.seen = {}


def lcm(*args):
    args = list(args)
    lcm = args.pop()
    for arg in args:
        lcm = (lcm * arg) // math.gcd(arg, lcm)
    return lcm


def part2(positions):
    moons = tuple(Moon(position, Point3d(0, 0, 0)) for position in positions)
    periods = {
        'x': PeriodTracker(),
        'y': PeriodTracker(),
        'z': PeriodTracker(),
    }
    steps = 0
    while any(p.length is None for p in periods.values()):
        for axis in ('x', 'y', 'z'):
            tracker = periods[axis]
            if tracker.length is not None:
                continue
            pos_and_vels = []
            for moon in moons:
                pos_and_vels.append((
                    getattr(moon.position, axis),
                    getattr(moon.velocity, axis)
                ))
            pos_and_vels = tuple(pos_and_vels)
            if pos_and_vels in tracker.seen:
                first = tracker.seen[pos_and_vels]
                tracker.first = first
                tracker.length = steps - first
            tracker.seen[pos_and_vels] = steps

        for moon_a, moon_b in itertools.combinations(moons, 2):
            moon_a.apply_gravity(moon_b)
        for moon in moons:
            moon.step()
        steps += 1
    assert all(t.first == 0 for t in periods.values())
    return lcm(*tuple(t.length for t in periods.values()))


def parse(line):
    match = re.match(
        r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>',
        line
    )
    return Point3d(*match.groups())


TEST1 = """<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>"""

TEST2 = """<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>"""

if __name__ == '__main__':
    assert part1(line_parser(TEST1, parse=parse), steps=10) == 179
    assert part2(line_parser(TEST1, parse=parse)) == 2772
    assert part2(line_parser(TEST2, parse=parse)) == 4686774924
    lines = line_parser(get_input(12, 2019), parse=parse)
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
