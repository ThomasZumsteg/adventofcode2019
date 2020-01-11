use common::get_input;
use common::int_code_computer::IntCodeComputer;

type Input = Vec<isize>;

fn part1(input: &Input) -> usize {
    let mut computer = IntCodeComputer::new(input);
    computer.input.push(1);
    while !computer.done {
        computer.step();
    }
    *computer.output.iter().skip_while(|&n| *n == 0).next().unwrap() as usize
}

fn part2(input: &Input) -> usize {
    let mut computer = IntCodeComputer::new(input);
    computer.input.push(5);
    while !computer.done {
        computer.step();
    }
    computer.output[0] as usize
}

fn parse(text: &str) -> Input {
    text.trim()
        .split(',')
        .map(|n| n.parse::<isize>().unwrap())
        .collect()
}

fn main() {
    let input = parse(&get_input(05, 2019));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
