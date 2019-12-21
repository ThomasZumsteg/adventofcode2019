"""Solution to day 20 of Advent of Code"""

import collections
import copy
import itertools
import re

from get_input import get_input, line_parser
from common import Point


def get_tag(point, lines, skip):
    if lines[point.y+1][point.x].isalpha():
        assert not lines[point.y][point.x+1].isalpha()
        diff = Point(0, 1)
    elif lines[point.y][point.x+1].isalpha():
        diff = Point(1, 0)
    else:
        raise Exception(f"No second char associated at {point}")
    tag = lines[point.y][point.x] + lines[point.y+diff.y][point.x+diff.x]
    skip.add(point+diff)

    before = point-diff
    after = point+Point(diff.x*2, diff.y*2)
    enter, exit = None, None
    if before.x >= 0 and before.y > 0 and\
            lines[before.y][before.x] == '.':
        exit = before
        enter = point
    elif 0 <= after.y < len(lines) and 0 <= after.x < len(lines[after.x]) and\
            lines[after.y][after.x] == '.':
        exit = after
        enter = point+diff
    else:
        raise Exception(f"No entry assosciated with tag {tag} at {point}")
    return tag, enter, exit


class Maze:
    def __init__(self, lines):
        self._map = {}
        self.portals = {}
        self.size = Point(len(lines[0]), len(lines))
        skip = set()
        for r, row in enumerate(lines):
            for c, char in enumerate(row):
                point = Point(c, r)
                if point in skip:
                    continue
                if char.isalpha():
                    char, enter, exit = get_tag(point, lines, skip)
                    point = enter
                    if char in self.portals:
                        inner_enter, inner_exit = self.portals[char]
                        if not self.is_inner(inner_enter):
                            inner_exit, exit = exit, inner_exit
                            inner_enter, enter = enter, inner_enter
                        assert self.is_inner(inner_enter) and\
                            not self.is_inner(enter)
                        self.portals[char] = {
                            inner_enter: (exit, +1),
                            enter: (inner_exit, -1),
                        }
                    else:
                        self.portals[char] = (enter, exit)
                self._map[point] = char

    def __getitem__(self, item):
        if isinstance(item, Point):
            return self._map[item]
        return NotImplemented

    def is_inner(self, point):
        return (
            4 < point.x <= self.size.x-4 and
            4 < point.y <= self.size.y-4
        )


def part1(lines):
    mapping = Maze(lines)
    no_exit, start = mapping.portals['AA']
    queue = [(start, 0)]
    seen = set([no_exit])
    while queue:
        pos, steps = queue.pop(0)
        if pos in seen:
            continue
        seen.add(pos)
        state = mapping[pos]
        if state in '#':
            continue
        if state == 'ZZ':
            return steps - 1
        if state in mapping.portals:
            queue.append((mapping.portals[state][pos][0], steps))
            continue
        assert state == '.'
        for diff in Point.directions:
            queue.append((pos+diff, steps+1))
    raise Exception("No path found")


def part2(lines):
    mapping = Maze(lines)
    no_exit, start = mapping.portals['AA']
    queue = [(start, 0, 0)]
    seen = set([(no_exit, 0)])
    while queue:
        pos, depth, steps = queue.pop(0)
        if (pos, depth) in seen:
            continue
        seen.add((pos, depth))
        state = mapping[pos]
        if state == 'ZZ' and depth == 0:
            return steps - 1
        if depth < 0 or state in ('#', 'AA', 'ZZ'):
            continue
        if state in mapping.portals:
            move, depth_diff = mapping.portals[state][pos]
            queue.append((move, depth+depth_diff, steps))
            continue
        assert state == '.'
        for diff in Point.directions:
            queue.append((pos+diff, depth, steps+1))
    raise Exception("No path found")


def parse(line):
    raise NotImplementedError


TEST1 = """
         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       
"""

TEST2 = """
                   A               
                   A               
  #################.#############  
  #.#...#...................#.#.#  
  #.#.#.###.###.###.#########.#.#  
  #.#.#.......#...#.....#.#.#...#  
  #.#########.###.#####.#.#.###.#  
  #.............#.#.....#.......#  
  ###.###########.###.#####.#.#.#  
  #.....#        A   C    #.#.#.#  
  #######        S   P    #####.#  
  #.#...#                 #......VT
  #.#.#.#                 #.#####  
  #...#.#               YN....#.#  
  #.###.#                 #####.#  
DI....#.#                 #.....#  
  #####.#                 #.###.#  
ZZ......#               QG....#..AS
  ###.###                 #######  
JO..#.#.#                 #.....#  
  #.#.#.#                 ###.#.#  
  #...#..DI             BU....#..LF
  #####.#                 #.#####  
YN......#               VT..#....QG
  #.###.#                 #.###.#  
  #.#...#                 #.....#  
  ###.###    J L     J    #.#.###  
  #.....#    O F     P    #.#...#  
  #.###.#####.#.#####.#####.###.#  
  #...#.#.#...#.....#.....#.#...#  
  #.#####.###.###.#.#.#########.#  
  #...#.#.....#...#.#.#.#.....#.#  
  #.###.#####.###.###.#.#.#######  
  #.#.........#...#.............#  
  #########.###.###.#############  
           B   J   C               
           U   P   P               
"""

TEST3="""
             Z L X W       C                 
             Z P Q B       K                 
  ###########.#.#.#.#######.###############  
  #...#.......#.#.......#.#.......#.#.#...#  
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
  #.#...#.#.#...#.#.#...#...#...#.#.......#  
  #.###.#######.###.###.#.###.###.#.#######  
  #...#.......#.#...#...#.............#...#  
  #.#########.#######.#.#######.#######.###  
  #...#.#    F       R I       Z    #.#.#.#  
  #.###.#    D       E C       H    #.#.#.#  
  #.#...#                           #...#.#  
  #.###.#                           #.###.#  
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#  
CJ......#                           #.....#  
  #######                           #######  
  #.#....CK                         #......IC
  #.###.#                           #.###.#  
  #.....#                           #...#.#  
  ###.###                           #.#.#.#  
XF....#.#                         RF..#.#.#  
  #####.#                           #######  
  #......CJ                       NM..#...#  
  ###.#.#                           #.###.#  
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#  
  #.....#        F   Q       P      #.#.#.#  
  ###.###########.###.#######.#########.###  
  #.....#...#.....#.......#...#.....#.#...#  
  #####.#.###.#######.#######.###.###.#.#.#  
  #.......#.......#.#.#.#.#...#...#...#.#.#  
  #####.###.#####.#.#.#.#.###.###.#.###.###  
  #.......#.....#.#...#...............#...#  
  #############.#.#.###.###################  
               A O F   N                     
               A A D   M                     
"""

if __name__ == '__main__':
    lines = line_parser(get_input(20, 2019), seperator='\n', parse=list)
    assert part1(line_parser(TEST1, parse=list)) == 23
    assert part1(line_parser(TEST2, parse=list)) == 58
    print(f"Part 1: {part1(lines)}")
    assert part2(line_parser(TEST3, parse=list)) == 396
    print(f"Part 2: {part2(lines)}")
