use common::get_input;

type Input = usize;

pub mod int_code_computer {
    use std::cell::{RefCell, RefMut};

    type Args = [isize];

    enum Result {
        Value(isize),
        None,
        Done,
    }

    pub struct IntCodeFunc<T>
        where T: IntCodeComputer, T: 'static {
        func: &'static dyn Fn(&mut T, &Args) -> Result,
        n_args: usize
    }

    pub trait IntCodeComputer {
        fn new(code: Vec<isize>) -> Self where Self: Sized;
        fn opcode(code: &usize) -> IntCodeFunc<Self> where Self: Sized;
        fn done(&self) -> RefMut<bool>;
        fn pointer(&self) -> RefMut<usize>;
        fn program(&self) -> RefMut<Vec<isize>>;

        fn step(&mut self) {
            let mut pointer = self.pointer();
            let code = self.program();
            *pointer += 1;
            let func = Self::opcode(&(code[*pointer] as usize));
            let mut args: Vec<isize> = Vec::with_capacity(func.n_args);
            for i in *pointer..(*pointer+func.n_args) {
                args.push(code[code[i] as usize]);
            }
            *pointer += func.n_args;
            let result = (*func.func)(self, &args);
            match result {
                Result::Value(value) => {
                    code[*pointer] = value;
                    *pointer += 1;
                },
                Result::Done => *self.done() = true,
                Result::None => {},
            }
        }
    }

    pub struct BasicIntCodeComputer {
        program: RefCell<Vec<isize>>,
        pointer: RefCell<usize>,
        done: RefCell<bool>,
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

        fn input(&mut self, _: &Args) -> Result {
            Result::Value(self.input.pop().unwrap())
        }

        fn output(&mut self, args: &Args) -> Result {
            self.output.push(args[0]);
            Result::Done
        }
    }

    impl IntCodeComputer for BasicIntCodeComputer {
        fn new(code: Vec<isize>) -> Self {
            BasicIntCodeComputer {
                program: RefCell::new(code),
                pointer: RefCell::new(0),
                done: RefCell::new(false),
                output: Vec::new(),
                input: Vec::new()
            }
        }

        fn done(&self) -> RefMut<bool> {
            self.done.borrow_mut()
        }

        fn pointer(&self) -> RefMut<usize> {
            self.pointer.borrow_mut()
        }

        fn program(&self) -> RefMut<Vec<isize>> {
            self.program.borrow_mut()
        }

        fn opcode(code: &usize) -> IntCodeFunc<Self> {
            match code % 100 {
                1 => IntCodeFunc { n_args: 2, func: &BasicIntCodeComputer::add },
                2 => IntCodeFunc { n_args: 2, func: &BasicIntCodeComputer::mult },
                3 => IntCodeFunc { n_args: 0, func: &BasicIntCodeComputer::input },
                4 => IntCodeFunc { n_args: 1, func: &BasicIntCodeComputer::output },
                99 => IntCodeFunc { n_args: 0, func: &BasicIntCodeComputer::done},
                _ => unimplemented!(),
            }
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
