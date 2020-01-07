use common::get_input;

type Input = usize;

pub mod int_code_computer {
    type Args = [isize];

    enum Result {
        Value(isize),
        None,
        Done,
    }

    pub struct IntCodeFunc {
        func: &'static dyn Fn(&mut dyn IntCodeComputer, &Args) -> Result,
        n_args: usize
    }

    pub trait IntCodeComputer {
        fn new(code: Vec<isize>) -> Self;
        fn opcode(code: &usize) -> IntCodeFunc;
        fn pointer(&mut self) -> &mut usize;
        fn done(&mut self) -> &mut bool;
        fn program(&mut self) -> &mut Vec<isize>;

        fn step(&mut self) {
            let mut program = self.program();
            let &mut pointer = self.pointer();
            let func_code = program[pointer] as usize;
            let func = Self::opcode(&func_code);
            pointer += 1;
            let mut args: Vec<isize> = Vec::with_capacity(func.n_args);
            for i in pointer..(pointer+func.n_args) {
                args.push(program[program[i] as usize]);
            }
            pointer += func.n_args;
            let result = (*func.func)(self, &args);
            match result {
                Result::Value(value) => {
                    let index = program[pointer] as usize;
                    program[index] = value;
                    pointer += 1;
                },
                Result::Done => *self.done() = true,
                Result::None => {},
            }
        }
    }

    pub struct BasicIntCodeComputer {
        program: Vec<isize>,
        pointer: usize,
        done: bool,
        output: Vec<isize>,
        input: Vec<isize>,
    }
    
    impl BasicIntCodeComputer {
        fn add(&mut self, args: &Args) -> Result {
            unimplemented!()
        }
    }

    impl IntCodeComputer for BasicIntCodeComputer {
        fn new(code: Vec<isize>) -> Self {
            BasicIntCodeComputer {
                program: code,
                pointer: 0,
                done: false,
                output: Vec::new(),
                input: Vec::new()
            }
        }

        fn done(&mut self) -> &mut bool {
            &mut self.done
        }

        fn pointer(&mut self) -> &mut usize {
            &mut self.pointer
        }

        fn program(&mut self) -> &mut Vec<isize> {
            &mut self.program
        }

        fn opcode(code: &usize) -> IntCodeFunc {
            match code {
                1 => IntCodeFunc { n_args: 2, func: Box::new(BasicIntCodeComputer::add) },
                _ => unimplemented!(),
            }
        }

// //         OpCodes!{
// //             1 => add(a, b) { Result::Value(a + b) };
// //             2 => mult(a, b) { Result::Value(a * b) };
// //             3 => input(self) { Result::Value(self.input.pop().unwrap()) };
// //             4 => output(self, a) { self.output.append(a); Result::None };
// //             99 => done() { Result::Done };
// //         }
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
