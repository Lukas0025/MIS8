NOP

; Load 2 numbers
LDI A, 0
LDI B, 127

; Mov test
MOV A, R0
  

; reg A with B to C
ADD A, B, C
SUB A, B, C
XOR A, B, D
AND A, B, D

; to variant
ADDTO A
SUBTO B
ANDTO C
XORTO D

; ALU Direct
ALU 0b111, C

; BUS
BUSW A, 0xFF
BUSR B, 0xFF

; Jumps tests
JMP     0xFA
JZ  R0, 0x0
JNZ A,  0x1