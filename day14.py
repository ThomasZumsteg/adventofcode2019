"""Solution to day 14 of Advent of Code"""

from get_input import get_input, line_parser

import collections


class Nanofactory:
    def __init__(self, lines):
        self.costs = {}
        for result, recipe in lines:
            assert result[1] not in self.costs
            self.costs[result[1]] = (result[0], recipe)

    def cost_to_produce_fuel(self, units=1):
        ore = 0
        state = collections.defaultdict(int)
        state['FUEL'] += units
        while any(value > 0 for value in state.values()):
            next_state = collections.defaultdict(int)
            for key, required in state.items():
                if key == 'ORE':
                    ore += required
                    continue
                produced, recipe = self.costs[key]
                ceil_div = -(-required // produced)
                for volume, component in recipe:
                    next_state[component] += volume * ceil_div
                next_state[key] += required - (produced * ceil_div)
            state = next_state
        return ore


def part1(lines):
    return Nanofactory(lines).cost_to_produce_fuel()


def part2(lines):
    factory = Nanofactory(lines)

    # Binary search
    target = 1000000000000
    (min_guess, max_guess) = (0, 1)

    while factory.cost_to_produce_fuel(units=max_guess) < target:
        (min_guess, max_guess) = (max_guess+1, 2*max_guess)
    while min_guess <= max_guess:
        guess = (min_guess + max_guess) // 2
        cost = factory.cost_to_produce_fuel(units=guess)
        if cost > target:
            max_guess = guess - 1
        elif cost == target:
            return guess
        else:
            min_guess = guess + 1
    return max_guess


def parse(line):
    recipe, result = line.split(' => ')
    components = []
    for component in recipe.split(', '):
        amount, ingredient = component.split(' ')
        components.append((int(amount), ingredient))
    amount, ingredient = result.split(' ')
    return ((int(amount), ingredient), tuple(components))


TEST1 = """157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"""


TEST2 = """2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF"""


if __name__ == '__main__':
    lines = line_parser(get_input(14, 2019), parse=parse)
    assert part1(line_parser(TEST1, parse=parse)) == 13312
    assert part1(line_parser(TEST2, parse=parse)) == 180697
    print(f"Part 1: {part1(lines)}")
    assert part2(line_parser(TEST1, parse=parse)) == 82892753
    assert part2(line_parser(TEST2, parse=parse)) == 5586022
    print(f"Part 2: {part2(lines)}")
