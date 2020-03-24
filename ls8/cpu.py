"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.stack_pointer = 0xF4 # F4 is ram address of 'Key Pressed'; stack ranges from F3 _downward_

    def ram_read(self, decimal_address):
        return self.ram[decimal_address]

    def ram_write(self, value, decimal_address):
        self.ram[decimal_address] = value

    def load(self, relative_file_path):
        """Load a program into memory."""

        address = self.pc

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
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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
            # ALU ops
            'MUL': 0b10100010,

            # PC mutators

            # Other
            'HLT': 0b00000001,
            'LDI': 0b10000010,
            'PRN': 0b01000111,
            'PUSH': 0b01000101,
            'POP': 0b01000110
        }
        
        # ALU ops
        def MUL():
            self.alu('MUL', 0, 1)

        # PC mutators

        # Other
        def HLT():
            sys.exit(0)

        def LDI(operand_a, operand_b):
            self.reg[operand_a] = operand_b

        def PRN(operand_a):
            print(self.reg[operand_a])
                   
        def PUSH(operand_a): # here, operand_a is a reg address
            self.stack_pointer -= 1
            self.ram[self.stack_pointer] = self.reg[operand_a]

        def POP(operand_a): # here too!
            self.reg[operand_a] = self.ram[self.stack_pointer]
            self.stack_pointer += 1

        branchtable = {
            # ALU ops
            ops['MUL']: MUL,

            # PC mutators

            # Other
            ops['HLT']: HLT,
            ops['LDI']: LDI,
            ops['PRN']: PRN,
            ops['PUSH']: PUSH,
            ops['POP']: POP
        }

        

        while True:
            IR = self.ram[self.pc] # Instruction Register

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            number_of_operands = IR >> 6

            if number_of_operands == 0 or (IR >> 5) & 1 == 1: # ALU operation
                branchtable[IR]()
            elif number_of_operands == 1:
                branchtable[IR](operand_a)
            elif number_of_operands == 2:
                branchtable[IR](operand_a, operand_b)

            self.pc += (number_of_operands + 1) # ensures pc is incremented appropriately

