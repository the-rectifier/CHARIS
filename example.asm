li r1, 0xa
li r2, 100
li r3, -19
add r4, r2, r1
sub r4, r1, r2
and r4, r4, r0
not r4, r4
or r4, r0, r1
nand r4, r1, r3
nor r4, r1, r4
sra r4, r3
srl r4, r3
sll r4, r3
rol r4, r3
ror r4, r3
lui r4, 0xffff
addi r4, r1, 0xfff6
nandi r4, r1, 0x0
ori r4, r1, 0x0
li r1, 0xffff
li r2, 0xa
sw r1, 10(r2)
lw r2, 0x2(r2)
sb r1, 0x0(r0)
lb r2, 0x0(r0)
beq r0, r0, 0x4
b 0x1
bne r0, r2, 0xfffe
