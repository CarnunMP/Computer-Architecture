"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

    def ram_read(self, decimal_address):
        return self.ram[decimal_address]

    def ram_write(self, value, decimal_address):
        self.ram[decimal_address] = value

    def load(self, relative_file_path):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        program = []
        
        with open(relative_file_path) as f:
            for line in f:
                if line[0] == "0" or line[0] == "1":
                    program.append(int(line[:8], 2))

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        ops = {
            'HLT': 0b00000001,
            'LDI': 0b10000010,
            'PRN': 0b01000111
        }

        while True:
            IR = self.ram[self.pc] # Instruction Register

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR == ops['HLT']:
                exit()

            elif IR == ops['LDI']:
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif IR == ops['PRN']:
                print(self.reg[operand_a])
                self.pc += 2

