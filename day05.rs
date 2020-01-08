use common::get_input;

type Input = usize;

pub mod int_code_computer {
    type Args = [isize];

    enum Result {
        Value(isize),
        Input(isize),
        Output(isize),
        None,
        Done,
    }

    pub struct IntCodeFunc<T> where T: IntCodeComputer {
        func: &'static dyn Fn(& mut T, &Args) -> Result,
        n_args: usize
    }

    pub trait IntCodeComputer {
        type Computer;

        fn new(code: Vec<isize>) -> Self::Computer;
        fn opcode(code: &usize) -> IntCodeFunc<Self::Computer>;
        fn done(&mut self) -> &mut bool;
        fn get_pointer(&self) -> usize;
        fn set_pointer(&mut self, pointer: usize);
        fn get_program_code(&self, index: usize) -> isize;
        fn set_program_code(&mut self, index: usize, value: isize);

        fn step(&mut self) {
            let mut pointer = self.get_pointer();
            let code = self.get_program_code(pointer) as usize;
            pointer += 1;
            let func = Self::opcode(&code);
            let mut args: Vec<isize> = Vec::with_capacity(func.n_args);
            for i in pointer..(pointer+func.n_args) {
                args.push(self.get_program_code(i));
            }
            pointer += func.n_args;
            let result = (*func.func)(self, &args);
            match result {
                Result::Value(value) => {
                    self.set_program_code(pointer, value);
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
            Result::Value(args[0] + args[1])
        }

        fn mult(&mut self, args: &Args) -> Result {
            Result::Value(args[0] * args[1])
        }

        fn done(&mut self, _: &Args) -> Result {
            Result::Done
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

        fn get_pointer(&self) -> usize {
            self.pointer
        }

        fn set_pointer(&mut self, pointer: usize) {
            self.pointer = pointer;
        }

        fn get_program_code(&self, pointer: usize) -> isize {
            self.program[pointer]
        }

        fn set_program_code(&mut self, pointer: usize, value: isize) {
            self.program[pointer] = value;
        }

        fn opcode(code: &usize) -> IntCodeFunc<Self> {
            match code {
                1 => IntCodeFunc { n_args: 2, func: &BasicIntCodeComputer::add },
                2 => IntCodeFunc { n_args: 2, func: &BasicIntCodeComputer::mult },
                99 => IntCodeFunc { n_args: 0, func: &BasicIntCodeComputer::done},
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
