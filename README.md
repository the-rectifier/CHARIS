# CHARIS 

Charis is a CHARISA assembler/disassembler written in Python

**CHARISA** stands for **CHA**nia **R**educed **I**nstruction **S**et **A**rchitecture and it's the instruction set of a MIPS like CPU for the Project of the Computer Organization Course (ACE312) at the Technical University of Crete. 

## Usage:
```python charis.py [-a] OR [-d] file```

## CPU Architecture:

- ```R0``` is a 32-bit Register Hardwired to ```0```
- 31 32-bit General Purpose Registers ```R1-R31```
- 2 Types of Instructions (R/I Type)
- Instructions **Always** 32 bits in length
- ALU Operations include: ```add, sub, nand, not, or, sra, sll, srl, ror, rol, li, addi, nandi, ori```
- 3 Types of Branching Instructions: ```b, bne, beq```
- 4 L/S Instructions: ```lw, sw, lb, sb```
- Byte addressable memory

## Instruction Synthesis

### R Type:

|6-bits|5-bits|5-bits|5-bits|5-bits|6-bits|
|------|------|------|------|------|------|
|OpCode|  Rs  |  Rd  |  Rt  |Unused| func |



### I Type:

|6-bits|5-bits|5-bits|16-bits|
|------|------|------|-------|
|OpCode|  Rs  |  Rd  | Immed |


## Example Assembly

```
li r1, 0xa
addi r2, 100
or r4, r0, r1
sw r1, 0x2(r2)
lw r1, 5(r8)
b 0x1
beq r0, r0, 0x4
```

Check [```example.asm```](https://github.com/the-rectifier/CHARIS/blob/master/example.asm) for all instructions.

[RTL notation for each instruction](https://github.com/the-rectifier/CHARIS/blob/master/CHARISA%20_RTL.pdf)

