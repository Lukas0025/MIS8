# Example ASM code
# read number form bus addr OxFF add +1 to this number and write to bus on OxFA

#read from bus
BUSR R0, 0xFF

#add 1
LDI R1, 1
ADDTO R0

#write to bus
BUSW R0, 0xFA

HALT

