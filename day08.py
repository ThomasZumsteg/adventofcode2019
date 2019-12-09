"""Solution to day 8 of Advent of Code"""

from get_input import get_input


def part1(lines, width=25, height=6):
    min_layer = min(
        (
            lines[i-width*height:i] for i in
            range(len(lines), 0, -width*height)
        ),
        key=lambda layer: layer.count('0')
    )
    return min_layer.count('1') * min_layer.count('2')


def part2(lines, width=25, height=6):
    layers = (
        lines[i-width*height:i] for i in
        range(len(lines), 0, -width*height)
    )
    base = next(layers)
    for layer in layers:
        base = [
            b if p == '2' else p
            for b, p in zip(base, layer)
        ]
    return '\n' + '\n'.join([
        ''.join('*' if p == '1' else ' ' for p in base[r:r+width])
        for r in range(0, len(base), width)])


if __name__ == '__main__':
    lines = tuple(get_input(8, 2019).strip())
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
