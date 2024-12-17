from dataclasses import dataclass
from sys import stdin


def main() -> None:
    cpu = Cpu.from_string(stdin.read())
    print(cpu)
    cpu.run()
    print("Part 1:", cpu.stdout())


REG_A: int = 4
REG_B: int = 5
REG_C: int = 6
REG: dict[str, int] = {"A": REG_A, "B": REG_B, "C": REG_C}


@dataclass
class Cpu:
    program: list[int]
    reg: dict[int, int]
    ip: int
    outbuf: list[int]

    @staticmethod
    def from_string(data: str) -> "Cpu":
        regstr, progstr = data.strip().split("\n\n")

        # initialize registers
        reg: dict[int, int] = dict()
        for line in regstr.strip().split("\n"):
            name: str = line[9]
            val: int = int(line.strip()[12:])
            reg[REG[name]] = val

        # read program
        program: list[int] = list(map(int, progstr[9:].strip().split(",")))

        return Cpu(program=program, reg=reg, ip=0, outbuf=[])

    def run(self) -> None:
        def combo(operand: int) -> int:
            return self.reg.get(operand, operand)

        while True:
            if self.ip >= len(self.program) - 1:
                break

            opcode, operand = self.program[self.ip], self.program[self.ip + 1]

            if opcode == 0:  # adv
                self.reg[REG_A] //= 2 ** combo(operand)
            elif opcode == 1:  # bxl
                self.reg[REG_B] ^= operand
            elif opcode == 2:  # bst
                self.reg[REG_B] = combo(operand) % 8
            elif opcode == 3:  # jnz
                if self.reg[REG_A] != 0:
                    self.ip = operand - 2
            elif opcode == 4:  # bxc
                self.reg[REG_B] ^= self.reg[REG_C]
            elif opcode == 5:  # out
                self.outbuf.append(combo(operand) % 8)
            elif opcode == 6:  # bdv
                self.reg[REG_B] = self.reg[REG_A] // 2 ** combo(operand)
            elif opcode == 7:  # cdv
                self.reg[REG_C] = self.reg[REG_A] // 2 ** combo(operand)

            self.ip += 2

    def stdout(self) -> str:
        return ",".join(str(n) for n in self.outbuf)


if __name__ == "__main__":
    main()
