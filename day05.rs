use common::get_input;

type Input = usize;

pub mod intCodeComputer {
    use std::collections::HashMap;

    type Args = [isize];
    enum Result {
        Value(isize),
        None,
        Done,
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
        pub output: Vec<isize>,
        pub input: Vec<isize>,
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
                output: Vec::new(),
                input: Vec::new(),
                opcodes: OpCodes! {
                    1 => add(2),
                    2 => mult(2),
                    3 => input(0),
                    4 => output(1),
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

        fn add(&mut self, args: &Args) -> Result {
            Result::Value(args[0] + args[1])
        }

        fn mult(&mut self, args: &Args) -> Result {
            Result::Value(args[0] * args[1])
        }

        fn output(&mut self, _: &Args) -> Result {
            Result::Value(self.output.pop().unwrap())
        }

        fn input(&mut self, args: &Args) -> Result {
            self.input.push(args[0]);
            Result::None
        }

        fn done(&mut self, _: &Args) -> Result {
            Result::Done
        }
    }

}

fn part1(input: &Input) -> usize {
    unimplemented!()
}

fn part2(input: &Input) -> usize {
    unimplemented!()
}

fn parse(text: &str) -> Input {
    unimplemented!()
}

fn main() {
    let input = parse(&get_input(05, 2019));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
