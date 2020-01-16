#! /usr/bin/python3
import numpy as np
from PIC19F84A_dat import*
## Program format : 
# byte : op(str) w(dec) data(dec) status=Z/DC/C(bin)
# bit  : op(str) data(bin) bit(dec) 
# jump : op(str)
# litteral : op(str) w(dec) data(dec) status=Z/DC/C(bin)
# control  : op(str) 


#### def : main program
def compile_program(program_file):
    lines    = load_program(program_file)
    obj_str  = compile_lines(lines)
    obj_file = write_out(program_file,obj_str)
    return obj_file


def encode_instr(instr_str):
    op = instr_str.split(" ")[0]
    if instruction_type[op] == 'byte' : 
        op,w,dat,st = instr_str.split(" ")
        dat,w,st = bin_s(dat),bin_s(w),st
        opcode   = instruction_set[op]
        op7      ='0'
    elif instruction_type[op] == 'bit' :
        op,dat,bit = instr_str.split(" ");bit = bin_s(bit,3)
        dat,w,st = dat, bin_s('0'),'000'
        opcode   = instruction_set[op]+bit[1:2]
        op7      = bit[0]
    elif instruction_type[op] == 'jump' :
        dat,w,st = bin_s('0'),bin_s('0'),bin_s('0',3)
        opcode = instruction_set[op]
        op7    = '0'
    elif instruction_type[op] == 'litteral' :
        op,dat,w,st = instr_str.split(" ")
        dat,w,st = bin_s(dat),bin_s(w),st
        opcode   = instruction_set[op]
        op7      ='0'
    elif instruction_type[op] == 'control' :
        dat,w,st = bin_s('0'),bin_s('0'),bin_s('0',3)
        opcode = instruction_set[op]
        op7    = '0'
    else :
        dat,st,w,opcode,op7=[""]*5
    instr = op7 + opcode + w + st + dat
    return instr
 
def load_program(program_file):
    program = open(program_file,'r')
    lines=program.read().splitlines();#print(lines)
    program.close()
    return lines
    
def compile_lines(lines,v=False):
    obj_str=""
    for instr_str in lines:
        if v : print(instr_str)
        instr_bin = encode_instr(instr_str);
        if v : print(instr_bin)
        if any(instr_bin):
            instr_hex = format(int(instr_bin,2),'x').zfill(7);
            if v : print(instr_hex)
            obj_str += instr_hex+"\n"           
    return obj_str
    
def write_out(program_file,obj_str):
    obj_file = program_file.replace('txt','out')
    obj = open(obj_file,"w")
    obj.write("v2.0 raw\n")
    obj.write(obj_str)
    obj.close()  
    print('%s' %(obj_file))     
    return obj_file   

#### def : misc 
def bin_s(x,fill=8):
    return format(int(x),'b').zfill(fill)

##################################################################
###### run 
if __name__== '__main__':
    program_file = ""
    if program_file=="" :
        program_file = 'program_test.txt'
    obj_file=compile_program(program_file)
    print('compilation sucess' ) 