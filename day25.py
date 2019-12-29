"""Solution to day 25 of Advent of Code"""

import collections
import itertools
import re

from get_input import get_input, line_parser
from common import (
        Done,
        IntcodeComputer,
        IntcodeComputerMeta,
    )


class IntcodeComputerDay25(IntcodeComputer):
    def __init__(self, code, *args, **kwargs):
        super().__init__(code, *args, **kwargs)
        self.relative_base = 0
        self.code = collections.defaultdict(int, enumerate(code))
        self._idle = 0

    @property
    def idle(self):
        return len(self.input) == 0 and self._idle > 2

    @property
    def args(self):
        args = []
        if self.func.needs_self:
            args.append(self)
        for n in range(self.func.n_args):
            mode = (self.code[self.pointer] // 10**(n+2)) % 10
            arg = self.code[self.pointer+1+n]
            if mode == 0:
                assert arg >= 0
                arg = self.code[arg]
            elif mode == 2:
                assert self.relative_base+arg >= 0
                arg = self.code[self.relative_base+arg]
            args.append(arg)
        return args

    def step(self):
        func = self.func
        # import pdb; pdb.set_trace()
        result = func(*self.args)
        if result is not None:
            assert isinstance(result, int)
            pos = self.code[self.pointer+1+func.n_args]
            if self.code[self.pointer] // 10**(2+self.func.n_args) == 2:
                pos += self.relative_base
            assert pos >= 0
            self.code[pos] = result
            self.pointer += 1
        self.pointer += 1 + func.n_args

    @IntcodeComputerMeta.opcode(1)
    def add(a, b):
        return a + b

    @IntcodeComputerMeta.opcode(2)
    def mult(a, b):
        return a * b

    @IntcodeComputerMeta.opcode(3)
    def input(self):
        if len(self.input) > 0:
            self._idle = 0
            return self.input.pop(0)
        self._idle += 1
        return -1

    @IntcodeComputerMeta.opcode(4)
    def output(self, a):
        self.output.append(a)

    @IntcodeComputerMeta.opcode(5)
    def jump_if_true(self, a, b):
        if a != 0:
            self.pointer = b - 3

    @IntcodeComputerMeta.opcode(6)
    def jump_if_false(self, a, b):
        if a == 0:
            self.pointer = b - 3

    @IntcodeComputerMeta.opcode(7)
    def less_than(a, b):
        return int(a < b)

    @IntcodeComputerMeta.opcode(8)
    def equals(a, b):
        return int(a == b)

    @IntcodeComputerMeta.opcode(9)
    def relative_base_offset(self, a):
        self.relative_base += a

    @IntcodeComputerMeta.opcode(99)
    def done(self):
        self.done = True
        raise Done


class Player:
    blacklist = set([
        'giant electromagnet',
        'infinite loop',
        'escape pod',
        'photons',
        'molten lava',
    ])

    directions = {
        "north": "south",
        "south": "north",
        "east": "west",
        "west": "east",
    }

    def __init__(self):
        self.seen = collections.defaultdict(set)
        self.room = None
        self.traceback = []
        self.to_take = []
        self.drop_order = None
        self.to_drop = None
        self.mode = 'EXPLORE'

    def read_room(self, text):
        varaibles = {}
        mode = None
        for line in text.splitlines():
            if line.startswith('== '):
                varaibles['ROOM'] = line[3:-3]
                self.room = varaibles
                mode = 'DESCRIPTION'
            elif mode == 'DESCRIPTION':
                varaibles[mode] = line
                mode = None
            elif line == 'Doors here lead:':
                mode = 'DOORS'
                varaibles[mode] = []
            elif mode == 'DOORS':
                if line == '':
                    mode = None
                else:
                    door = line[2:]
                    varaibles[mode].append(door)
            elif line == 'Items here:':
                mode = 'ITEMS'
                varaibles[mode] = []
            elif mode == 'ITEMS':
                if line == '':
                    mode = None
                else:
                    item = line[2:]
                    if item not in self.blacklist:
                        self.to_take.append(f"take {item}")
                    varaibles[mode].append(item)
            elif line == 'Items in your inventory:':
                mode = 'INV'
                self.room[mode] = set()
            elif mode == 'INV':
                if line == '':
                    mode = None
                else:
                    self.room[mode].add(line[2:])

    def get_command(self):
        if self.mode == 'EXPLORE':
            return self._explore()
        if self.mode == 'TO_SCALE':
            return self._to_scale()
        if self.mode == 'PASS_SCALE':
            return self._pass_scale()

    def _explore(self):
        self.mode = 'EXPLORE'
        for item in self.room.get('ITEMS', []):
            if item not in self.blacklist:
                self.room['ITEMS'].remove(item)
                return f'take {item}\n'
        if self.traceback:
            self.seen[self.room['ROOM']]\
                .add(self.traceback[-1])
        for door in self.room['DOORS']:
            room = self.room['ROOM']
            if door not in self.seen[room]:
                self.seen[room].add(door)
                self.traceback.append(self.directions[door])
                return door + '\n'
        if self.traceback != []:
            return self.traceback.pop() + '\n'
        return self._to_scale()

    def _to_scale(self):
        self.mode = 'TO_SCALE'
        if self.to_room != []:
            return self.to_room.pop(0) + '\n'
        if 'INV' not in self.room:
            return 'inv\n'
        if self.drop_order is None:
            self.drop_order = []
            for n in range(0, len(self.room['INV'])):
                for subset in itertools.combinations(self.room['INV'], n):
                    self.drop_order.append(subset)
        return self._pass_scale()

    def _pass_scale(self):
        self.mode = 'PASS_SCALE'
        assert self.room['ROOM'] == 'Security Checkpoint'
        if self.to_drop is None:
            self.to_drop = list(self.drop_order.pop())
        for item in self.room.get('ITEMS', []):
            if item not in self.blacklist:
                self.room['ITEMS'].remove(item)
                return f'take {item}\n'
        if self.to_drop != []:
            return 'drop ' + self.to_drop.pop(0) + '\n'
        self.to_drop = None
        return 'west\n'


def part1(code):
    computer = IntcodeComputerDay25(code)
    player = Player()
    lines = []
    while True:
        try:
            computer.step()
        except Done:
            break
        if computer.output and computer.output[-1] == ord('\n'):
            line = ''.join(chr(c) for c in computer.output)
            # print(line, end='')
            m = re.search(r'typing (\d+) on the keypad', line)
            if m:
                return m.group(1)
            if line == 'Command?\n':
                player.read_room(''.join(lines).strip())
                if 'pressure-sensitive' in player.room['DESCRIPTION']:
                    if player.traceback != []:
                        player.to_room = [
                            player.directions[t] for t in player.traceback
                        ]
                command = player.get_command()
                # print(command, end='')
                computer.input.extend(ord(c) for c in command)
                lines.clear()
            lines.append(line)
            computer.output.clear()


if __name__ == '__main__':
    lines = line_parser(get_input(25, 2019), seperator=',')
    print(f"Part 1: {part1(lines)}")
