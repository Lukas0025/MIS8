#!/usr/bin/python3

import re
import sys, getopt
from intelhex import IntelHex

##
# All MIS8 OPS
#
OPS = [
    "NOP",
    "MOV",
    "BUSW",
    "BUSR",
    "ALU",
    "JMP",
    "JZ",
    "JNZ",
    "LDI",
    "HALT"
]

##
# Registers names
#
REGS = [
    "A",
    "B",
    "C",
    "D",
    "R0",
    "R1",
    "R2",
    "R3"
]

##
# Types of output files
#
O_TYPES = [
    "BYTEARRAY",
    "VHDL",
    "TXTBIN",
    "BIN",
    "HEX"
]

##
# Macros
# can by edited
#
MACROS = {
    'ADD A B'  :'ALU 0b000',
    'ADDTO'    :'ALU 0b000',
    'SUB A B'  :'ALU 0b010',
    'SUBTO'    :'ALU 0b010',
    'AND A B'  :'ALU 0b100',
    'ANDTO'    :'ALU 0b100',
    'XOR A B'  :'ALU 0b110',
    'XORTO'    :'ALU 0b110'
}

##
# End program with error
# @param line number of line with error
# @param msg message of error
#
def end_error(line, msg):
    print("compile error on line {} : {}".format(line, msg))
    exit(1)

##
# Convert number to binary format (signed)
# @param integer integer to convert
# @param digits number of bits
# @return string of binary number
#
def int2bin(integer, digits):
    if integer >= 0:
        return bin(integer)[2:].zfill(digits)
    else:
        return bin(2**digits + integer)[2:]

##
# Get address of register name
# @param name name of register (A, B, C, D, R0, ...)
# @return string of binary address
#
def get_reg(name):
    if   ((name == "A") or (name == "R0")):
        return "00"
    elif ((name == "B") or (name == "R1")):
        return "01"
    elif ((name == "C") or (name == "R2")):
        return "10"
    elif ((name == "D") or (name == "R3")):
        return "11"

##
# Check is valid 10b address
# @param line number of line if fail to note this line to user
# @param address address reprezented as any number in any base
#
def is_valid_addr(line, address):
    addr = int2bin(to_num(line, address), 10)
    return len(addr) <= 10

##
# Check is ALU OP is valid ALU OP
# @param line number of line if fail to note this line to user
# @param op operation for ALU
#
def is_valid_alu_op(line, op):
    addr = int2bin(to_num(line, op), 3)
    return len(addr) <= 3

##
# Convert int in any base to base 10
# @param line number of line if fail to note this line to user
# @param string string of number
# @return int
#
def to_num(line, string):
    try:
        return int(string, 0)
    except:
        end_error(line, "invalid number {}".format(string))

##
# Read args
#
O_TYPE  = "HEX"
infile  = None
outfile = None

try:
    opts, args = getopt.getopt(sys.argv[1:], "hi:o:f:", ["ifile=", "ofile=", "format="])
except getopt.GetoptError:
    print('{} -i <inputfile> -o <outputfile> [-f <format>]'.format(sys.argv[0]))
    print('use -h parameter for help')
    sys.exit(2)

for opt, arg in opts:
    if opt == '-h':
        print('{} -i <inputfile> -o <outputfile> [-f <format>]'.format(sys.argv[0]))
        print('Compile input ASM file to output binary file platform MIS8')
        print()
        print('-i, --infile     Input ASM file')
        print('-o, --ofile      Output file')
        print('-f, --format     Format of output file [HEX, BIN, TXTBIN, VHDL, BYTEARRAY] default is HEX')
        sys.exit()
    elif opt in ("-i", "--ifile"):
        infile  = arg
    elif opt in ("-o", "--ofile"):
        outfile = arg
    elif opt in ("-f", "--format"):
        O_TYPE  = arg.upper()

##
# Check if args is set
#
if ((infile is None) or (outfile is None)):
    print('{} -i <inputfile> -o <outputfile> [-f <format>]'.format(sys.argv[0]))
    print('use -h parameter for help')
    sys.exit(2)

if (O_TYPE not in O_TYPES):
    print('not supported format')
    sys.exit(3)


##
# Open file
#
AsmFile = open(infile, 'r')
Lines = AsmFile.readlines()


##
# Code generating part
#
line_num = 0
code     = []
for line in Lines:

    line = re.sub(' +', ' ', line).replace(",", "").upper()

    for k, v in MACROS.items():
        line = line.replace(k, v)

    line      = line.split()
    line_num += 1

    inst = []
    for word in line:
        # comments break
        if (word.startswith(";")):
            break
        
        if (word.startswith("#")):
            break

        inst.append(word)

    # no inscruction on line
    if len(inst) == 0:
        continue

    if (inst[0] not in OPS):
        end_error(line_num, "unknown inscruction {}".format(inst[0]))

    if (inst[0] == "NOP"):
        if (len(inst) != 1):
            end_error(line_num, "bad arguments count for NOP")

        code.append("00000000")
        
    elif (inst[0] == "MOV"):
        if (len(inst) != 3):
            end_error(line_num, "bad arguments count for MOV")

        if (inst[1] not in REGS) or (inst[2] not in REGS):
            end_error(line_num, "invalid register name for MOV")

        code.append("001{}{}0".format( get_reg(inst[1]), get_reg(inst[2]) ))

    elif (inst[0] == "BUSW"):
        if (len(inst) != 3):
            end_error(line_num, "bad arguments count for BUSW")

        if (inst[1] not in REGS):
            end_error(line_num, "invalid register name for BUSW")

        if (not is_valid_addr(line_num, inst[2])):
            end_error(line_num, "invalid address for BUSW")

        addr = int2bin(to_num(line, inst[2]), 10)

        code.append("0101{}{}".format(get_reg(inst[1]),  addr[0:2]))
        code.append(addr[2:])

    elif (inst[0] == "BUSR"):
        if (len(inst) != 3):
            end_error(line_num, "bad arguments count for BUSR")

        if (inst[1] not in REGS):
            end_error(line_num, "invalid register name for BUSR")

        if (not is_valid_addr(line_num, inst[2])):
            end_error(line_num, "invalid address for BUSR")

        addr = int2bin(to_num(line, inst[2]), 10)

        code.append("0100{}{}".format(get_reg(inst[1]),  addr[0:2]))
        code.append(addr[2:])

    elif (inst[0] == "ALU"):
        if (len(inst) != 3):
            end_error(line_num, "bad arguments count for ALU")

        if (inst[2] not in REGS):
            end_error(line_num, "invalid register name for ALU")

        if (not is_valid_alu_op(line_num, inst[1])):
            end_error(line_num, "invalid OP for ALU")

        op = int2bin(to_num(line_num, inst[1]), 3)

        code.append("011{}{}".format(get_reg(inst[2]),  op))
        
    elif (inst[0] == "JMP"):
        if (len(inst) != 2):
            end_error(line_num, "bad arguments count for JMP")

        if (not is_valid_addr(line_num, inst[1])):
            end_error(line_num, "invalid address for JMP")

        addr = int2bin(to_num(line, inst[1]), 10)

        code.append("100000{}".format(addr[0:2]))
        code.append(addr[2:])

    elif (inst[0] == "JZ"):
        if (len(inst) != 3):
            end_error(line_num, "bad arguments count for JZ")

        if (inst[1] not in REGS):
            end_error(line_num, "invalid register name for JZ")

        if (not is_valid_addr(line_num, inst[2])):
            end_error(line_num, "invalid address for JZ")

        addr = int2bin(to_num(line, inst[2]), 10)

        code.append("101{}1{}".format(get_reg(inst[1]), addr[0:2]))
        code.append(addr[2:])

    elif (inst[0] == "JNZ"):
        if (len(inst) != 3):
            end_error(line_num, "bad arguments count for JNZ")

        if (inst[1] not in REGS):
            end_error(line_num, "invalid register name for JNZ")

        if (not is_valid_addr(line_num, inst[2])):
            end_error(line_num, "invalid address for JNZ")

        addr = int2bin(to_num(line, inst[2]), 10)

        code.append("101{}0{}".format(get_reg(inst[1]), addr[0:2]))
        code.append(addr[2:])

    elif (inst[0] == "LDI"):
        if (len(inst) != 3):
            end_error(line_num, "bad arguments count for LDI")

        if (inst[1] not in REGS):
            end_error(line_num, "invalid register name for LDI")

        if (to_num(line_num, inst[2]) not in range(-128, 128)):
            end_error(line_num, "invalid number to write to REG using LDI")

        code.append("110{}000".format(get_reg(inst[1])))
        code.append(int2bin(to_num(line_num, inst[2]), 8))

    elif (inst[0] == "HALT"):
        if (len(inst) != 1):
            end_error(line_num, "bad arguments count for HALT")

        code.append("11111111")


##
# END Code generating part
#

##
# Convert binary back to decimaly
#

for i in range(len(code)):
    code[i] = int(code[i], 2)

##
# Save code to file
#
if (O_TYPE  ==  "BYTEARRAY"):
    with open(outfile, 'w') as f:
        sys.stdout = f
        print(code)

elif (O_TYPE == "VHDL"):
    with open(outfile, 'w') as f:
        sys.stdout = f

        print("(")
        
        for inst in code:
            print("\"{}\",".format(int2bin(inst, 8)))

        print(")")

elif (O_TYPE == "TXTBIN"):
    with open(outfile, 'w') as f:
        sys.stdout = f

        for inst in code:
            print(int2bin(inst, 8))

elif (O_TYPE == "BIN"):
    ih = IntelHex()

    for i in range(len(code)):
        ih[i] = code[i]

    ih.tobinfile(outfile)

elif (O_TYPE == "HEX"):
    ih = IntelHex()

    for i in range(len(code)):
        ih[i] = code[i]

    ih.tofile(outfile, format="hex")