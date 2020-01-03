use common::get_input;

type Input = (usize, usize);

trait Digits {
    fn as_digits(number: &usize) -> Self;
    fn incr(&self) -> Self;
    fn has_doubles(&self) -> bool;
    fn as_usize(&self) -> usize;
}

impl Digits for Vec<usize> {
    fn as_digits(number: &usize) -> Self {
        let digits: Vec<char> = number.to_string().chars().collect();
        let mut iter = digits.iter()
            .map(|d| d.to_string().parse::<usize>().unwrap());
        let mut prev = iter.next().unwrap();
        let mut result = vec![prev];
        for d in iter {
            if d > prev {
                prev = d;
            }
            result.push(prev);
        }
        result
    }

    fn incr(&self) -> Self {
        let next = self.as_usize() + 1;
        Self::as_digits(&next)
    }

    fn has_doubles(&self) -> bool {
        let mut iter = self.iter();
        let mut last = iter.next().unwrap();
        for next in iter {
            if next == last {
                return true
            }
            last = next;
        }
        false
    }

    fn as_usize(&self) -> usize {
        self.iter()
            .fold(String::new(), |acc, d| acc + &d.to_string())
            .parse::<usize>()
            .unwrap()
    }
}

fn part1(input: &Input) -> usize {
    let (start, end) = input;
    let mut digits: Vec<usize> = <Vec<usize>>::as_digits(start);
    let mut total = 0;
    while digits.as_usize() < *end {
        println!("{}", digits.as_usize());
        if digits.has_doubles() {
            total += 1;
        }
        digits = digits.incr();
    }
    total
}

fn part2(input: &Input) -> usize {
    unimplemented!()
}

fn parse(text: &str) -> Input {
    let parts = text.trim().split('-')
        .map(|n| n.parse::<usize>().unwrap())
        .collect::<Vec<usize>>();
    assert!(parts.len() == 2);
    (parts[0], parts[1])
}

fn main() {
    let lines = parse(&get_input(4, 2019));
    println!("Part 1: {}", part1(&lines));
    println!("Part 2: {}", part2(&lines));
}

