from dataclasses import dataclass
from sys import stdin


def main() -> None:
    raw_input: str = stdin.read()
    cpu = Cpu.from_string(raw_input)
    cpu.run()
    print("Part 1:", cpu.stdout())
    print("Part 2:", find_a(cpu))


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


def find_a(cpu: Cpu) -> int:
    a, _ = solve_next_a(cpu)
    return a


def solve_next_a(cpu: Cpu, a: int = 0) -> tuple[int, bool]:
    """
    Reverse engineering the source program for part 2 reveals that:
    * The program is one big loop, jumping back to the beginning on the last
      instruction
    * REG_A is the only variable that affects the loop condition
    * REG A's value is only manipulated by dividing by 8 on each iteration.
    * Each iteration of the program takes exactly 3 bits from A and manipulates the
      value in various ways in different registers, before printing out a number
      based on those bits.

    Because we can partition A so cleanly into independent chunks of 3 bits at a
    time, we can solve it 3 bits at a time and get immediate feedback on if those
    3 bits are plausible or not. This is significantly easier than guessing the
    whole number at once.
    """
    for n in range(8):
        candidate_a: int = (a << 3) | n
        cpu.reg[REG_A] = candidate_a
        cpu.reg[REG_B] = 0
        cpu.reg[REG_C] = 0
        cpu.outbuf = []
        cpu.ip = 0
        cpu.run()

        if cpu.outbuf == cpu.program:
            # Found the solution!
            return candidate_a, True
        elif cpu.program[-len(cpu.outbuf) :] == cpu.outbuf:
            # Produced end of the program correctly, this value is promising
            final_a, found = solve_next_a(cpu, candidate_a)
            if found:
                return final_a, True

    # Ran out of things to try...
    return 0, False


if __name__ == "__main__":
    main()
