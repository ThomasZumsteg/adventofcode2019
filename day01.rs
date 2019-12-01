use common::get_input;

type Input = Vec<isize>;

fn part1(input: &Input) -> isize {
    input.iter().fold(0, |acc, line| line / 3 - 2 + acc)
}

fn get_fuel(start: isize) -> isize {
    let mut total = 0;
    let mut stage = start / 3 - 2;
    while stage > 0 {
        total += stage;
        stage = stage / 3 - 2;
    }
    total
}

fn part2(input: &Input) -> isize {
    input.iter().map(|&l| get_fuel(l)).sum()
}

fn parse(text: String) -> Input {
    text.trim()
        .split('\n')
        .map(|l| l.parse::<isize>().unwrap())
        .collect()
}

fn main() {
    let input = parse(get_input(01, 2019));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
