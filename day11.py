"""Solution to day 11 of Advent of Code"""

import collections


from common import Point
from day09 import IntcodeComputerDay9, Done
from get_input import get_input, line_parser


class Painter:
    def __init__(self, position, heading):
        self.position = position
        self.heading = heading


def part1(code):
    ship = collections.defaultdict(list)
    robot = Painter(position=Point(0, 0), heading=Point(0, 1))
    computer = IntcodeComputerDay9(code.copy())
    while True:
        colors = ship[robot.position]
        computer.input.append(colors[-1] if colors else 0)
        try:
            while len(computer.output) < 2:
                computer.step()
        except Done:
            break
        color, turn = computer.output.pop(0), computer.output.pop(0)
        ship[robot.position].append(color)
        if turn == 0:
            robot.heading = robot.heading.turn_left()
        elif turn == 1:
            robot.heading = robot.heading.turn_right()
        else:
            raise NotImplementedError
        robot.position += robot.heading
    return sum(1 for colors in ship.values() if len(colors) > 0)


def part2(code):
    ship = collections.defaultdict(int)
    robot = Painter(position=Point(0, 0), heading=Point(0, 1))
    computer = IntcodeComputerDay9(code.copy())
    ship[Point(0, 0)] = 1
    while True:
        computer.input.append(ship[robot.position])
        try:
            while len(computer.output) < 2:
                computer.step()
        except Done:
            break
        color, turn = computer.output.pop(0), computer.output.pop(0)
        ship[robot.position] = color
        if turn == 0:
            robot.heading = robot.heading.turn_left()
        elif turn == 1:
            robot.heading = robot.heading.turn_right()
        else:
            raise NotImplementedError
        robot.position += robot.heading
    white_spaces = [p for p, v in ship.items() if v == 1]
    xs = [p.x for p in white_spaces]
    ys = [p.y for p in white_spaces]
    output = []
    for y in reversed(range(min(ys), max(ys)+1)):
        output.append('\n')
        for x in reversed(range(min(xs), max(xs)+1)):
            output.append('*' if ship[Point(x, y)] == 1 else ' ')
    return ''.join(output)


if __name__ == "__main__":
    lines = line_parser(get_input(11, 2019), seperator=',')
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
