#!/usr/bin/python
# Author: Odysseas Stavrou 
# Github: odysseassu@gmail.com
'''
CHania Reduced Instruction Set Architecture
Assembler / Disassembler

Usage: python charis.py [-a] OR [-d] file

Assemble:
outputs a rom.data file with the 32-bit binary representation of the input file

Disassemble:
outputs a rom.data.dis file with the disassembled instructions
'''
import os
import sys
import struct
import argparse
import textwrap

# change this to reflect the TOTAL lines of code + memory init
# extra lines beyond the resulting assembled instructions are initialized as 0 
LINES = 1024

SHAMT = '00000'
R_opcode = '100000' 


# R_type = {'add', 'sub', 'and', 'or', 'nand', 'nor', 'sra', 'srl', 'sll', 'ror', 'rol', 'not'}
# I_type = {'li', 'lui', 'addi', 'nandi', 'ori', 'b', 'beq', 'bne', 'lb', 'sw', 'sb', 'lw'}
single_reg = {'not', 'rol', 'ror', 'sra', 'srl', 'sll'}


ISA_I_Type = {
    'li': '111000',
    'lui': '111001',
    'addi': '110000',
    'nandi': '110010',
    'ori': '110011',
    'b': '111111',
    'beq': '000000',
    'bne': '000001',
    'lb': '000011',
    'sb': '000111',
    'lw': '001111',
    'sw': '011111'
    }
ISA_R_Type = {
    'add': '110000',
    'sub': '110001',
    'and': '110010',
    'or': '110011',
    'not': '110100',
    'nand': '110101',
    'nor': '110110',
    'sra': '111000',
    'srl': '111001',
    'sll': '111010',
    'rol': '111100',
    'ror': '111101'
    }
ISA_D = {
    '100000': 'R',
    '111000': 'li',
    '111001': 'lui',
    '110000': 'addi',
    '110010': 'nandi',
    '110011': 'ori',
    '111111': 'b',
    '000000': 'beq',
    '000001': 'bne',
    '000011': 'lb',
    '000111': 'sb',
    '001111': 'lw',
    '011111': 'sw'
    }
ISA_R_Type_D = {
    '110000': 'add',
    '110001': 'sub',
    '110010': 'and',
    '110011': 'or',
    '110100': 'not',
    '110101': 'nand',
    '110110': 'nor',
    '111000': 'sra',
    '111001': 'srl',
    '111010': 'sll',
    '111100': 'rol',
    '111101': 'ror'
    }

def sign_extend(value): 
    if value[:2] == '0x':
        value = value[2:]
        bin_value = ''.join([bin(int(x, 16))[2:].zfill(4) for x in value])
        if len(bin_value) < 16:
            bin_value = (16-len(bin_value))* '0' + bin_value
    else:
        value = struct.pack('>h',int(value))
        bin_value = ''.join([f'{byte:0>8b}' for byte in value])
    
    assert(len(bin_value) == 16)
    return bin_value
    

def assembler(line):
    inst = line.split(' ')[0]
    args = [x.replace(' ', '').strip(',') for x in line.split(' ')][1:]
    immed = 0
    rd = 0
    rs = 0
    if inst in ISA_R_Type:
        if len(args) == 3:
            # add, sub, and, or, nand, nor
            # add r3, r4, r5
            rd = bin(int(args[0].strip('r')))[2:].zfill(5)
            rs = bin(int(args[1].strip('r')))[2:].zfill(5)
            rt = bin(int(args[2].strip('r')))[2:].zfill(5)
            return R_opcode + rs + rd + rt + SHAMT + ISA_R_Type.get(inst)
        elif len(args) == 2:
            # not, sra, sll, srl, rol, ror
            # not r4 r5
            rt = '00000'
            rd = bin(int(args[0].strip('r')))[2:].zfill(5)
            rs = bin(int(args[1].strip('r')))[2:].zfill(5)
            return R_opcode + rs + rd + rt + SHAMT + ISA_R_Type.get(inst)

    elif inst in ISA_I_Type:
        if len(args) == 1:
            # b -2
            rs = '00000'
            rd = '00000'
            immed = sign_extend(args[0])
        elif len(args) == 2:
            if inst == 'sw' or inst == 'sb' or inst == 'lw' or inst == 'lb':
                # lw r4, 5(r6)
                # args = [r4, 5(r6)]
                rd = bin(int(args[0].strip('r')))[2:].zfill(5)
                immed, rs = args[1].strip(')').split('(')
                rs = bin(int(rs.strip('r')))[2:].zfill(5)
                immed = sign_extend(immed)
            else:
                # li r4, 19
                rd = bin(int(args[0].strip('r')))[2:].zfill(5)
                rs = '00000'
                immed = sign_extend(args[1])
        elif len(args) == 3:
            # addi r4, r5, 139
            rs = bin(int(args[1].strip('r')))[2:].zfill(5)
            rd = bin(int(args[0].strip('r')))[2:].zfill(5)
            immed = sign_extend(args[2])
        return ISA_I_Type.get(inst) + rs + rd + immed
    else:
        print('Unsupported Instruction!')
        return


def assemble(file):
    instructions = []
    count = 0
    with open(file, 'r') as f:
        inst = f.readline().strip('\n')
        while inst != '':
            instructions.append(inst)
            inst = f.readline().strip('\n')

    with open('rom.data', 'w') as f:
        for idx, inst in enumerate(instructions):
            x = assembler(inst)
            if len(x) != 32:
                print(f'Error Assembling instruction {instructions[idx]}')
            else:
                print(f'{hex(count)}: {instructions[idx]} ----------------> 0x{hex(int(x, 2))[2:].zfill(8)}')
                count += 4
                f.write(x + '\n')
        for _ in range(LINES - len(instructions)):
            f.write('0' * 32 + '\n')


def dis(mc):
    op_code = ISA_D.get(mc[0:6])  # 6
    rs = int(mc[6:11], 2)  # 5
    rd = int(mc[11:16], 2)  # 5
    rt = int(mc[16:21], 2)
    func = ISA_R_Type_D.get(mc[26:32])
    immed = hex(int(mc[16:], 2))

    if op_code == 'R':
        if func in single_reg:
            return f'{func} r{rd}, r{rs}'
        return f'{func} r{rd}, r{rs}, r{rt}'
    else:
        if op_code == 'li' or op_code == 'lui':
            return f'{op_code} r{rd}, {immed}'
        elif op_code == 'b':
            return f'{op_code} {immed}'
        elif op_code == 'beq' or op_code == 'bne' or op_code == 'ori' or op_code == 'addi' or op_code == 'nandi':
            return f'{op_code} r{rd}, r{rs}, {immed}'
        elif op_code == 'lw' or op_code == 'sw' or op_code == 'sb' or op_code == 'lb':
            return f'{op_code} r{rd}, {immed}(r{rs})'


def disassemble(file):
    count = 0
    machine_code = []
    with open(file, 'r') as f:
        mc = f.readline().strip('\n')
        while mc != '':
            machine_code.append(mc)
            mc = f.readline().strip('\n')

    with open(file + '.dis', 'w') as f:
        for mc in machine_code:
            asm = dis(mc)
            print(f'{hex(count)}: 0x{hex(int(mc, 2))[2:].zfill(8)} ------------> {asm}')
            count += 4
            f.write(asm + '\n')


def pass_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            CHAR-ISA Assembler / Disassembler
            CHania Reduced Instruction Set Architecture
            '''
        ),
        epilog='Written By Odysseas Stavrou',
        usage='python charis.py [-a] OR [-d] file')
    parser.add_argument('-a', '--assemble', action='store_true', required=False, help='Assemble .asm file')
    parser.add_argument('-d', '--disassemble', action='store_true', required=False, help='Disassemble .rom file')
    parser.add_argument('file', type=str, help='File to proccess')
    args = parser.parse_args()
    input_file = args.file

    if args.assemble and args.disassemble:
        print('Please supply args -a OR -d')
        sys.exit(-1)
    if args.assemble:
        assemble(input_file)
    elif args.disassemble:
        disassemble(input_file)
    else:
        print('Please supply args -a or -d')
        sys.exit(-1)


if __name__ == '__main__':
    pass_args()
