use common::get_input;

type Input = Vec<isize>;


pub mod intCodeComputer {
    use std::collections::HashMap;

    type Args = [isize];
    enum Result {
        Value(isize),
        Done
    }

    struct IntCodeFunc {
        func: &'static dyn Fn(&Args) -> Result,
        n_args: usize
    }

    pub struct IntCodeComputer {
        pub program: Vec<isize>,
        pointer: usize,
        opcodes: HashMap<usize, IntCodeFunc>,
        pub done: bool,
    }

    macro_rules! OpCodes(
        { $($code:expr => $func:ident ( $n_args:expr )),+ } => {
            {
                let mut m: HashMap<usize, IntCodeFunc> = HashMap::new();
                $(
                    let func = IntCodeFunc {
                        func: &$func,
                        n_args: $n_args,

                    };
                    m.insert($code, func);
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
                done: false,
                opcodes: OpCodes! {
                    1 => add(2),
                    2 => mult(2),
                    99 => done(0)
                }
            }
        }

        pub fn step(&mut self) {
            let func_code = self.program[self.pointer] as usize;
            let func = self.opcodes.get(&func_code).unwrap();
            self.pointer += 1;
            let mut args: Vec<isize> = Vec::with_capacity(func.n_args);
            for i in self.pointer..(self.pointer+func.n_args) {
                args.push(self.program[self.program[i] as usize]);
            }
            self.pointer += func.n_args;
            let result = (*func.func)(&args);
            match result {
                Result::Value(value) => {
                    let index = self.program[self.pointer] as usize;
                    self.program[index] = value;
                    self.pointer += 1;
                },
                Result::Done => self.done = true,
            }
        }
    }

    fn add(args: &Args) -> Result {
        Result::Value(args[0] + args[1])
    }

    fn mult(args: &Args) -> Result {
        Result::Value(args[0] * args[1])
    }

    fn done(_: &Args) -> Result {
        Result::Done
    }

}

fn part1(code: &Input) -> isize {
    let mut computer = intCodeComputer::IntCodeComputer::new(code.clone());
    computer.program[1] = 12;
    computer.program[2] = 2;
    while !computer.done {
        computer.step();
    }
    computer.program[0]
}

fn part2(code: &Input) -> isize {
    for noun in 1.. {
        for verb in 1..noun+1 {
            let mut computer = intCodeComputer::IntCodeComputer::new(code.clone());
            computer.program[1] = noun;
            computer.program[2] = verb;
            while !computer.done {
                computer.step();
            }
            if computer.program[0] == 19690720 {
                return 100 * noun + verb
            }
        }
    }
    panic!("Cannot find solution")
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
