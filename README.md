# MIS8
Instruction set for minimalistic processors

### Install ASM compilator to PC

```sh
sudo make install
```

need packages `python3` and `python3-pip`

### Using ASM compilator

```sh
mis8_asm -i <inputfile> -o <outputfile> [-f <format>]

-i, --infile     Input ASM file
-o, --ofile      Output file
-f, --format     Format of output file [HEX, BIN, TXTBIN, VHDL, BYTEARRAY] default is HEX
```

ASM description is in `ASM.md`

### Registers

| BIN         | NAME     | USED AS     |
| ----------- | -------- |------------ |
| 00          | A        | ALU A INPUT |
| 01          | B        | ALU B INPUT |
| 10          | C        |             |
| 11          | D        |             |

### Instruction set table

| ASM         | Pseudo code                       | OP Code |   Binary               |
| ----------- | --------------------------------- |---------|------------------------|
| NOP         |                                   |   000   | `000X XXXX`            |
| MOV         | REG(S) => REG(D)                  |   001   | `001S SDDX`            |
| BUS         | BUS(A) <=> REG(R) (w=1 for write) |   010   | `010W RRAA AAAA AAAA`  |
| ALU         | REG(D) <= ALU(REG(0), REG(1), O)  |   011   | `011R ROOO`            |
| JMP         | PC <= A                           |   100   | `100X XXAA AAAA AAAA`  |
| JZ/JNZ      | PC <= if REG(R) == 0 (I=1 -> not) |   101   | `101R RIAA AAAA AAAA`  |
| LDI         | REG(R) <= C                       |   110   | `110R RXXX CCCC CCCC`  |
| HALT        | PC <= PC                          |   111   | `111X XXXX`            |

### Instructions

X - don't care

U - unused

#### NOP
| BIT |  7  |  6  |  5  |  4  |  3  |  2  |  1  |  0  |  7  |  6  |  5  |  4  |  3  |  2  |  1  |  0  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | 0   | 0   | 0   | X   | X   | X   | X   |  X  | U   | U   | U   | U   | U   | U   | U   | U   |

Do nothing

#### MOV
| BIT |  7  |  6  |  5  |  4  |  3  |  2  |  1  |  0  |  7  |  6  |  5  |  4  |  3  |  2  |  1  |  0  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | 0   | 0   | 1   | S   | S   | D   | D   |  X  | U   | U   | U   | U   | U   | U   | U   | U   |

> SS and DD used as unsigned index to register file

Move content of register SS to register DD

#### BUS
| BIT |  7  |  6  |  5  |  4  |  3  |  2  |  1  |  0  |  7  |  6  |  5  |  4  |  3  |  2  |  1  |  0  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | 0   | 1   | 0   | W   | R   | R   | A   |  A  | A   | A   | A   | A   | A   | A   | A   | A   |

> AAAAAAAAAA used as 10bit address for BUS

> RR used as unsigned index to register file

> W is one bit direction selector

Move content of register RR to BUS on AAAAAAAAAA address if W is 1

Move content of BUS on AAAAAAAAAA address to register RR if W is 0

#### ALU
| BIT |  7  |  6  |  5  |  4  |  3  |  2  |  1  |  0  |  7  |  6  |  5  |  4  |  3  |  2  |  1  |  0  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | 0   | 1   | 1   | R   | R   | O   | O   |  O  | U   | U   | U   | U   | U   | U   | U   | U   |

> OOO used as OP for ALU unit

> RR used as unsigned index to register file

> Default alu have 000 ADD, 010 SUB, 100 AND, 110 XOR

Do ALU operation with register 0 (A) and 1 (B) and save result to RR register

#### JMP
| BIT |  7  |  6  |  5  |  4  |  3  |  2  |  1  |  0  |  7  |  6  |  5  |  4  |  3  |  2  |  1  |  0  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | 1   | 0   | 0   | X   | X   | X   | A   |  A  | A   | A   | A   | A   | A   | A   | A   | A   |

> AAAAAAAAAA used as 10bit address for next inscriction to exec

Jump to inscruction on AAAAAAAAAA address. (Set PC to AAAAAAAAAA)

#### JZ/JNZ
| BIT |  7  |  6  |  5  |  4  |  3  |  2  |  1  |  0  |  7  |  6  |  5  |  4  |  3  |  2  |  1  |  0  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | 1   | 0   | 1   | R   | R   | JZ  | A   |  A  | A   | A   | A   | A   | A   | A   | A   | A   |

> AAAAAAAAAA used as 10bit address for next inscriction to exec

> if JZ = 1 then work as JZ else as JNZ

> RR used as unsigned index to register file

#### LDI
| BIT |  7  |  6  |  5  |  4  |  3  |  2  |  1  |  0  |  7  |  6  |  5  |  4  |  3  |  2  |  1  |  0  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | 1   | 1   | 0   | R   | R   | X   | X   |  X  | C   | C   | C   | C   | C   | C   | C   | C   |

> CCCCCCCC used as 8bit signed integer

> RR used as unsigned index to register file

Set CCCCCCCC number to RR register

#### HALT
| BIT |  7  |  6  |  5  |  4  |  3  |  2  |  1  |  0  |  7  |  6  |  5  |  4  |  3  |  2  |  1  |  0  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | 1   | 1   | 1   | X   | X   | X   | X   |  X  | U   | U   | U   | U   | U   | U   | U   | U   |

Stop processor work can start again only after reset
