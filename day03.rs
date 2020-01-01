use std::collections::HashMap;

use common::get_input;
use common::point::Point;

type Input = Vec<Vec<(String, usize)>>;

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
    result
}

struct Wire {
    name: String,
    path: HashMap<Point, usize>,
}

impl Wire {
    fn new(name: String, path: &Vec<(String, usize)>) -> Wire {
        let mut result = Wire { name: name, path: HashMap::new() };
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
                result.path.insert(location, step);
            }
        }
        result
    }

    fn intersection(&self, other: &Wire) -> HashMap<Point, HashMap<String, usize>> {
        let mut intersections: HashMap<Point, HashMap<String, usize>> = HashMap::new();
        for (point, self_value) in &self.path {
            if let Some(other_value) = other.path.get(point) {
                let mut inter = HashMap::new();
                inter.insert(other.name.clone(), other_value.clone());
                inter.insert(self.name.clone(), self_value.clone());
                intersections.insert(point.clone(), inter);
            }
        }
        intersections
    }
}

fn part1(paths: &Input) -> usize {
    let mut wires: Vec<Wire> = Vec::new();
    for (p, path) in paths.iter().enumerate() {
        let wire = Wire::new(format!("{}", p), path);
        wires.push(wire);
    }
    let intersections = wires[0].intersection(&wires[1]);
    let mut result: Option<usize> = None;
    for point in intersections.keys() {
        if result.is_none() || result.unwrap() > (point.x.abs() + point.y.abs()) as usize {
            result = Some((point.x.abs() + point.y.abs()) as usize)
        }
    }
    result.unwrap()
}

fn part2(wires: &Input) -> usize {
    unimplemented!()
}

fn main() {
    let input = parse(&get_input(3, 2019));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
