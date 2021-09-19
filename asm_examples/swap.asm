# Example ASM code
# swap R0 content with R1 content (XCHG)

# using 3 registers
mov A, C
mov B, A
mov C, B

# using xor
xorto A
xorto B
xorto A
