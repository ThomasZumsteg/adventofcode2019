use std::collections::{HashMap, HashSet};

use common::get_input;
use common::point::Point;

type WirePath = HashMap<Point, HashSet<usize>>;
type Input = (WirePath, WirePath);

trait Wire {
    fn create_wire(path: &Vec<(String, usize)>) -> Self;
    fn intersections(&self, other: &Self) -> HashSet<Point>;
}

impl Wire for HashMap<Point, HashSet<usize>> {
    fn create_wire(path: &Vec<(String, usize)>) -> Self {
        let mut result = HashMap::new();
        let mut step: usize = 0;
        let mut location: Point = Point::new(0, 0);
        for (direction, steps) in path {
            let diff = match direction.as_ref() {
                "U" => Point::new(0, 1),
                "D" => Point::new(0, -1),
                "R" => Point::new(1, 0),
                "L" => Point::new(-1, 0),
                _ => panic!("Not a known letter"),
            };
            for _ in 0..*steps {
                step += 1;
                location = location + diff;
                let steps = result.entry(location).or_insert(HashSet::new());
                steps.insert(step);
            }
        }
        result
    }

    fn intersections(&self, other: &Self) -> HashSet<Point> {
        let mut intersections: HashSet<Point> = HashSet::new();
        for point in self.keys() {
            if other.contains_key(&point) {
                intersections.insert(point.clone());
            }
        }
        intersections
    }
}

fn part1(paths: &Input) -> usize {
    let intersections = paths.0.intersections(&paths.1);
    let mut result: Option<usize> = None;
    for point in intersections {
        if result.is_none() || result.unwrap() > (point.x.abs() + point.y.abs()) as usize {
            result = Some((point.x.abs() + point.y.abs()) as usize)
        }
    }
    result.unwrap()
}

fn part2(paths: &Input) -> usize {
    let (wire_a, wire_b) = paths;
    let intersections = wire_a.intersections(&wire_b);
    let mut result: Option<usize> = None;
    for point in intersections {
        let local_min = wire_a[&point].iter().min().unwrap() + wire_b[&point].iter().min().unwrap();
        if result.is_none() || local_min < result.unwrap() {
            result = Some(local_min);
        }
    }
    result.unwrap()
}

fn parse(text: &str) -> Input {
    let mut result = Vec::new();
    for line in text.trim().split('\n') {
        let mut row = Vec::new();
        for element in line.split(',') {
            row.push((
                element[0..1].to_string(),
                element[1..].parse().unwrap(),
            ));
        }
        result.push(row);
    }
    assert!(result.len() == 2);
    (HashMap::create_wire(&result[0]), HashMap::create_wire(&result[1]))
}


fn main() {
    let input = parse(&get_input(3, 2019));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
