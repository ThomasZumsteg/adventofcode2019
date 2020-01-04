use common::get_input;

type Input = (usize, usize);

trait Digits {
    fn as_digits(number: &usize) -> Self;
    fn incr(&self) -> Self;
    fn has_doubles(&self) -> bool;
    fn as_usize(&self) -> usize;
    fn exactly_one_double(&self) -> bool;
}

impl Digits for Vec<usize> {
    fn as_digits(number: &usize) -> Self {
        number.to_string().chars()
            .map(|d| d.to_string().parse::<usize>().unwrap())
            .collect()
    }

    fn incr(&self) -> Self {
        let next = self.as_usize() + 1;
        let digits = <Vec<usize>>::as_digits(&next);
        let mut iter = digits.iter();
        let mut prev = iter.next().unwrap();
        let mut result: Vec<usize> = vec![prev.clone()];
        for d in iter {
            if d > prev {
                prev = d;
            }
            result.push(prev.clone());
        }
        result
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

    fn exactly_one_double(&self) -> bool {
        let mut iter = self.iter();
        let mut last = iter.next().unwrap();
        let mut run = 1;
        for next in iter {
            if next == last {
                run += 1;
            } else {
                if run == 2 {
                    return true;
                }
                run = 1;
                last = next;
            }
        }
        run == 2
    }
}

fn part1(input: &Input) -> usize {
    let (start, end) = input;
    let mut digits: Vec<usize> = <Vec<usize>>::as_digits(start);
    let mut total = 0;
    while digits.as_usize() < *end {
        if digits.has_doubles() {
            total += 1;
        }
        digits = digits.incr();
    }
    total
}

fn part2(input: &Input) -> usize {
    let (start, end) = input;
    let mut digits: Vec<usize> = <Vec<usize>>::as_digits(start);
    let mut total = 0;
    while digits.as_usize() < *end {
        if digits.exactly_one_double() {
            total += 1;
        }
        digits = digits.incr();
    }
    total
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

