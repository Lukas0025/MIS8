# MIS8 ASM
Instruction set for minimalistic processors

### Install ASM compilator to PC

```sh
sudo make install
```

need packages `python3` and `python3-pip`

### uninstall ASM compilator to PC

```sh
sudo make uninstall
```

### Using ASM compilator

```sh
mis8_asm -i <inputfile> -o <outputfile> [-f <format>]

-i, --infile     Input ASM file
-o, --ofile      Output file
-f, --format     Format of output file [HEX, BIN, TXTBIN, VHDL, BYTEARRAY] default is HEX
```

### Registers

| NAME     | USED AS     |
| -------- |------------ |
| A or R0  | ALU A INPUT |
| B or R1  | ALU B INPUT |
| C or R2  |             |
| D or R3  |             |

### Instructions table

| ASM         | Pseudo code                             |
| ----------- | --------------------------------------- |
| NOP         |                                         |
| MOV S, D    | REG(S) => REG(D)                        |
| BUSW R, A   | BUS(A) <= REG(R)                        |
| ALU O, R    | REG(R) <= ALU(REG(0), REG(1), O)        |
| ADDTO R     | REG(R) <= REG(0) + REG(1)               |
| ADD A, B, R | REG(R) <= REG(0) + REG(1)               |
| SUBTO R     | REG(R) <= REG(0) - REG(1)               |
| SUB A, B, R | REG(R) <= REG(0) - REG(1)               |
| ANDTO R     | REG(R) <= REG(0) AND REG(1)             |
| AND A, B, R | REG(R) <= REG(0) AND REG(1)             |
| XORTO R     | REG(R) <= REG(0) XOR REG(1)             |
| XOR A, B, R | REG(R) <= REG(0) XOR REG(1)             |
| JMP A       | [Inscruction address] <= A              |
| JZ R, A     | [Inscruction address] <= if REG(R) == 0 |
| JNZ R, A    | [Inscruction address] <= if REG(R) != 0 |
| LDI R, C    | REG(R) <= C                             |
| HALT        | Stop work                               |

### Exmaple code

```asm
# Example ASM code
# cout R0 to 100

LDI A, 0 # 0,1 (2BYTES)
LDI B, 1 # 2,3 (2BYTES) <-- Jump here

ADDTO A  # 4 (1BYTE)

# compare with 100
LDI B, 100
SUBTO C
JNZ C, 2

# counting is done
HALT
```

compiled with

```sh
mis8_asm -i jump.asm -o out.txt -f txtbin
```

content of out.txt (after run command)

```bin
11000000
00000000
11001000
00000001
01100000
11001000
01100100
01110010
10110000
00000010
11111111
```

more asm examples is in `asm_examples`