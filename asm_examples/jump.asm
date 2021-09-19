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