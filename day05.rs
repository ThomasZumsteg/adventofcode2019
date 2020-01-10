use common::get_input;

type Input = Vec<isize>;

pub mod int_code_computer {
    type Args = [isize];

    enum Result {
        Value(isize),
        None,
        Done,
    }

    pub struct IntCodeFunc {
        func: &'static dyn Fn(&mut IntCodeComputer, &Args) -> Result,
        n_args: usize
    }

    pub struct IntCodeComputer {
        program: Vec<isize>,
        pointer: usize,
        pub done: bool,
        pub output: Vec<isize>,
        pub input: Vec<isize>,
    }

    impl IntCodeComputer {
        pub fn new(code: &Vec<isize>) -> Self {
            IntCodeComputer {
                program: code.clone(),
                pointer: 0,
                done: false,
                output: Vec::new(),
                input: Vec::new()
            }
        }

        pub fn step(&mut self) {
            print!("{:?} -> {:?} ", self.pointer, self.program[self.pointer] % 100);
            let code = self.program[self.pointer] as usize;
            let func = IntCodeComputer::opcode(&code);
            self.pointer += 1;
            let mut args: Vec<isize> = Vec::with_capacity(func.n_args);
            for i in 0..func.n_args {
                let arg = match (code as isize) / 10_isize.pow((i+2) as u32) % 10 {
                    0 => self.program[self.pointer],
                    1 => self.program[self.program[self.pointer] as usize],
                    _ => unimplemented!(),
                };
                args.push(self.program[self.program[self.pointer + i] as usize]);
            }
            println!("{:?}", args);
            self.pointer += func.n_args;
            let result = (*func.func)(self, &args);
            match result {
                Result::Value(value) => {
                    let index = self.program[self.pointer] as usize;
                    self.program[index] = value;
                    self.pointer += 1;
                },
                Result::Done => self.done = true,
                Result::None => {},
            }
        }

        fn add(&mut self, args: &Args) -> Result {
            Result::Value(args[0] + args[1])
        }

        fn mult(&mut self, args: &Args) -> Result {
            Result::Value(args[0] * args[1])
        }

        fn done(&mut self, _: &Args) -> Result {
            Result::Done
        }

        fn input(&mut self, _: &Args) -> Result {
            Result::Value(self.input.pop().unwrap())
        }

        fn output(&mut self, args: &Args) -> Result {
            self.output.push(args[0]);
            Result::None
        }

        fn opcode(code: &usize) -> IntCodeFunc {
            match code % 100 {
                1 => IntCodeFunc { n_args: 2, func: &IntCodeComputer::add },
                2 => IntCodeFunc { n_args: 2, func: &IntCodeComputer::mult },
                3 => IntCodeFunc { n_args: 0, func: &IntCodeComputer::input },
                4 => IntCodeFunc { n_args: 1, func: &IntCodeComputer::output },
                99 => IntCodeFunc { n_args: 0, func: &IntCodeComputer::done},
                _ => unimplemented!(),
            }
        }
    }
}

fn part1(input: &Input) -> usize {
    let mut computer = int_code_computer::IntCodeComputer::new(input);
    computer.input.push(1);
    while !computer.done {
        computer.step();
    }
    *computer.output.iter().take_while(|&n| *n == 0).next().unwrap() as usize
}

fn part2(input: &Input) -> usize {
    unimplemented!()
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
