'''
compiler.py *file*.apl [-v] [-e]
    example : 
./compiler.py programs/add.apl -e
'''
#! /usr/bin/python3
import numpy as np
import pandas as pd
import sys,os
from glob_colors import*
appolo_folder=os.path.dirname(__file__)
df_PROM=pd.read_pickle(appolo_folder+'/dat/PROM.pkl')


#### def : main program
def compile_program(program_file,v=False,e=False):
    lines    = load_program(program_file)
    instructions,labels = get_instruction_labels(lines,v)
    obj_str  = compile_instructions(instructions,labels,e)
    obj_file = write_out(program_file,obj_str)
    return obj_file

def encode_instr(instr_str,labels):
    op,dat = instr_str.split(" ")[:2]
    if 'JUMP' in op :
        dat=labels[dat]
        loadwl,acc  = df_PROM.loc['LOADWL']['opcode'],format(int(dat/16),'x')
        jump,data = df_PROM.loc[op]['opcode'],format(int(dat%16),'x')
        instr = loadwl+acc + ' ' + jump+data
    else : 
        opcode,data = df_PROM.loc[op]['opcode'],format(int(dat),'x')
        instr = opcode + data
    return instr

#####
def load_program(program_file):
    program = open(program_file,'r')
    lines=program.read().splitlines();#print(lines)
    program.close()
    return lines
    
def get_instruction_labels(lines,v=False) : 
    labels,l,instructions = dict(),0,[]
    for line in lines : 
        line = line.split("#")[0].split(':')
        if len(line)>1 : 
            lab,instr = line
        else : 
            lab,instr = '',line[0]
        op = instr.split(" ")[0]
        if op in df_PROM.index : 
            if lab : labels[lab] = l
            instructions.append(instr);l+=1
    if v : print(yellow+'program preprocess : \n'+red+'\n'.join(map(lambda a,b:str(a)+' '+b,range(len(instructions)),instructions))+black);print(yellow+'labels:'+blue,labels,black)
    return instructions,labels
    
def compile_instructions(instructions,labels,v=False) : 
    obj_str=""
    # add 1 to label lines after jump instructions (since they are 2 clock cycles)
    labelsJump = dict.copy(labels)
    for instr_str,l in zip(instructions,range(len(instructions))) : 
        if 'JUMP' in instr_str.split(" ")[0] :
            for lab,val in labels.items() : 
                if val > l : labelsJump[lab] += 1;#print(instr_str,lab,labelsJump[lab])
    # encode instructions
    if v : print(yellow+'Encoding : \n'+'label'.ljust(7)+'instr'.ljust(12)+'hex'.ljust(7)+'addr'+black);l0=0
    for instr_str,l in zip(instructions,range(len(instructions))):
        if instr_str == 'END' : break
        instr_hex = encode_instr(instr_str,labelsJump)
        obj_str += instr_hex+"\n"
        if v :
            lab = ''.join([key  for (key,val) in labels.items() if val==l])
            print(blue+lab.ljust(7) + red+instr_str.ljust(12) + green+instr_hex.ljust(7)+magenta+hex(l0)+black)
            l0 += int(len(instr_hex)/2)
    return obj_str
    
def write_out(program_file,obj_str) : 
    folder = os.path.dirname(os.path.realpath(program_file))
    obj_file = folder+'/bin/'+os.path.basename(program_file).replace('.apl','.out')
    obj = open(obj_file,"w")
    obj.write("v2.0 raw\n")
    obj.write(obj_str)
    obj.close()
    print(green+"compilation sucess. binary file in :\n"+yellow+'%s' %(obj_file)+black)
    return obj_file

##################################################################
###### run 
if __name__== '__main__':
    args=sys.argv
    if len(args)>1 : 
        program_file = args[1]
        verbose = '-v' in args or '--verbose' in args
        encode  = '-e' in args or '--encode' in args
    else : 
        program_file = appolo_folder+'/dat/add.apl'
    obj_file=compile_program(program_file,v=verbose,e=encode)