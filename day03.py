import re
from dataclasses import dataclass
from sys import stdin
from typing import Optional, Type

RE_MUL = re.compile(r"mul\((\d+),(\d+)\)")
RE_INSTR = re.compile(r"don't\(\)|do\(\)|mul\(\d+,\d+\)")


def main() -> None:
    program_string = stdin.read()
    print("Part 1:", MulComputer(program_string).run())
    print("Part 2:", Computer(program_string).run())


class Instruction:
    @staticmethod
    def from_string(s: str) -> Optional["Instruction"]:
        pass


@dataclass
class Mul(Instruction):
    a: int
    b: int

    @staticmethod
    def from_string(s: str) -> Optional[Instruction]:
        if mo := RE_MUL.match(s):
            return Mul(*map(int, mo.groups()))
        return None


class Do(Instruction):
    @staticmethod
    def from_string(s: str) -> Optional[Instruction]:
        if s == "do()":
            return Do()
        return None


class Dont(Instruction):
    @staticmethod
    def from_string(s: str) -> Optional[Instruction]:
        if s == "don't()":
            return Dont()
        return None


class Computer:
    instruction_classes: list[Type[Instruction]] = [Mul, Do, Dont]

    def __init__(self, program: str) -> None:
        self.enable_multiplication = True
        self.program: list[Instruction] = [
            Computer.string_to_instr(s)
            for line in program.split()
            for s in RE_INSTR.findall(line)
        ]

    def is_multiplication_enabled(self) -> bool:
        return self.enable_multiplication

    def run(self) -> int:
        self.enable_multiplication = True

        total = 0
        for instr in self.program:
            if isinstance(instr, Do):
                self.enable_multiplication = True
            elif isinstance(instr, Dont):
                self.enable_multiplication = False
            elif isinstance(instr, Mul) and self.is_multiplication_enabled():
                total += instr.a * instr.b
        return total

    @staticmethod
    def string_to_instr(s: str) -> Instruction:
        for instruction_class in Computer.instruction_classes:
            if instr := instruction_class.from_string(s):
                return instr
        raise Exception(f"Unsupported instruction {s}")


class MulComputer(Computer):
    def is_multiplication_enabled(self) -> bool:
        return True


if __name__ == "__main__":
    main()
