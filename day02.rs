use common::get_input;

type Input = Vec<isize>;


pub mod IntCodeComputer {
    use std::collections::HashMap;

    type Args = [isize];
    type Result = Option<isize>;
    type IntCodeFunc = dyn Fn(&Args) -> Result;

    pub struct IntCodeComputer {
        pub program: Vec<isize>,
        pointer: usize,
        opcodes: HashMap<usize, &'static IntCodeFunc>,
    }

    macro_rules! OpCodes(
        { $($code:expr => $func:ident),+ } => {
            {
                let mut m: HashMap<usize, &IntCodeFunc> = HashMap::new();
                $(
                    m.insert($code, &$func);
                )+
                m
            }
        };
    );

    impl IntCodeComputer {
        pub fn new(code: Vec<isize>) -> IntCodeComputer {
            IntCodeComputer {
                program: code,
                pointer: 0,
                opcodes: OpCodes! {
                    1 => add,
                    2 => mult,
                    99 => done
                }
            }
        }

        pub fn step(&mut self) -> Result {
            let func_code = self.program[self.pointer] as usize;
            let func = self.opcodes.get(&func_code).unwrap();
            self.pointer += 1;
            unimplemented!()
        }
    }

    fn add(args: &Args) -> Result {
        Some(args[0] + args[1])
    }

    fn mult(args: &Args) -> Result {
        Some(args[0] * args[1])
    }

    fn done(_: &Args) -> Result {
        None
    }

}

fn part1(code: &Input) -> isize {
    let mut computer = IntCodeComputer::IntCodeComputer::new(code.clone());
    loop {
        if computer.step().is_none() {
            break
        }
    }
    computer.program[0]
}

fn part2(code: &Input) -> isize {
    unimplemented!()
}

fn parse(text: &str) -> Input {
    text.trim()
        .split(',')
        .map(|n| n.parse::<isize>().unwrap())
        .collect()
}

fn main() {
    let input = parse(&get_input(02, 2019));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
