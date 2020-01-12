use common::get_input;

use std::collections::{HashMap, HashSet, VecDeque};

type Input = HashMap<String, String>;

fn part1(orbit_map: &Input) -> usize {
    let mut orbit_count = 0;
    for orbit in orbit_map.keys()  {
        let mut orbiter = orbit;
        while orbit_map.contains_key(orbiter) {
            orbiter = orbit_map.get(orbiter).unwrap();
            orbit_count += 1;
        }
    }
    orbit_count
}

fn part2(orbits: &Input) -> usize {
    let mut orbit_map = HashMap::new();
    for (a, b) in orbits {
        orbit_map.entry(a).or_insert(HashSet::new()).insert(b);
        orbit_map.entry(b).or_insert(HashSet::new()).insert(a);
    }
    let goal = orbit_map.get(&"SAN".to_string()).unwrap().iter().next().unwrap();
    let start = orbit_map.get(&"YOU".to_string()).unwrap().iter().next().unwrap();
    let mut queue = VecDeque::new();
    let mut seen: HashSet<String> = HashSet::new();
    queue.push_back((0, start));
    while !queue.is_empty() {
        let (steps, current) = queue.pop_front().unwrap();
        if current == goal {
            return steps
        }
        if seen.contains(*current) {
            continue
        }
        seen.insert((*current).clone());
        for step in orbit_map.get(current).unwrap() {
            queue.push_back((steps+1, step));
        }
    }
    panic!("Unable to find a solution");
}

fn parse(text: &str) -> Input {
    let mut orbit_map = HashMap::new();
    for line in text.trim().split('\n') {
        let mut parts = line.trim().split(')');
        let a = parts.next().unwrap();
        let b = parts.next().unwrap();
        assert!(parts.next().is_none());
        orbit_map.insert(b.to_string(), a.to_string());
    }
    orbit_map
}

fn main() {
    let input = parse(&get_input(06, 2019));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
