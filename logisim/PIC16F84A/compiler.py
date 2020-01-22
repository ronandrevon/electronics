#! /usr/bin/python3
import numpy as np
import pandas as pd
from glob_colors import*
import os,sys
'''
   Program format : 
byte     : op(str) address(<80) d(boolean)
bit      : op(str) address(<80) bit(<8)
jump     : op(str) address(<1024)
literal  : op(str) data(<255)
control  : op(str)
'''
PIC_folder=os.path.dirname(__file__)
df_PROM=pd.read_pickle(PIC_folder+'/dat/PROM.pkl')
instruction_type = df_PROM['type']
opcode  = df_PROM['opcode']
SFR     = ['INDF','TMR0','OPTION','PCL','STATUS','FSR','PORTA','TRISA','PORTB','TRISB','EEDATA','EECON1','EEADR','EECON2','PCLATH','INTCON']

#### def : main program
def compile_program(program_file,v=False,e=False):
    lines    = load_program(program_file)
    lines,lab,var = preprocess_lines(lines,verbose)
    obj_str  = compile_lines(lines,lab,var,e)
    obj_file = write_out(program_file,obj_str)
    return obj_file

########
def preprocess_lines(lines,verbose=False) : 
    labels,l,var,instructions = dict(),0,[],[]
    for line in lines : 
        line = line.split("#")[0].split(':')
        if len(line)>1 : 
            lab,instr = line
        else : 
            lab,instr = '',line[0]
        op = instr.split(" ")[0]
        if op in df_PROM.index : 
            if lab : labels[lab] = l
            instructions.append(instr.replace('  ',''));l+=1
            if instruction_type[op] in ['byte','bit','mem'] : 
                var.append( instr.split(" ")[1])
    var = [v for v in np.unique(var) if v not in SFR]
    var_dict = dict(zip(['INDF','PCL','STATUS','FSR','PCLATH','INTCON'],[0,2,3,4,10,11]))
    var_dict.update(dict(zip(['TMR0'  ,'TRISA','TRISB','EECON1','EECON2'],[1,5,6,8,9])))
    var_dict.update(dict(zip(['OPTION','PORTA','PORTB','EEDATA','EEADR' ],[1,5,6,8,9])))
    var_dict.update(dict(zip(np.unique(var),np.arange(len(var))+12)))
    if verbose : 
        print(yellow+'program preprocess : ')
        print(red+'\n'.join(map(lambda a,b:str(a)+' '+b,range(len(instructions)),instructions))+black);
        print(yellow+'labels:'+blue,labels,yellow+'variables:'+blue,var,black)
        print(yellow+'instructions '+red,np.unique([i.split(' ')[0] for i in instructions]),black)
    return instructions,labels,var_dict
    
def encode_instr(instr_str,labels,var):
    op = instr_str.split(" ")[0]
    if instruction_type[op] == 'byte' :
        op,f,d = instr_str.split(" ")[:3]
        instr = opcode[op] + d + bin_s(var[f],7)
    elif instruction_type[op] == 'mem' :
        op,f = instr_str.split(" ")[:2]
        instr = opcode[op] + bin_s(var[f],7)
    elif instruction_type[op] == 'bit' :
        op,f,b = instr_str.split(" ")[:3]
        instr = opcode[op] + bin_s(b,3) + bin_s(var[f],7)
    elif instruction_type[op] == 'jump' :
        op,a = instr_str.split(" ")[:2]
        instr = opcode[op] + bin_s(labels[a],11)
    elif instruction_type[op] == 'literal' :
        op,k = instr_str.split(" ")[:2]
        instr = opcode[op] + bin_s(k,8)
    elif instruction_type[op] == 'control' :
        instr = opcode[op]
    return instr
    
def load_program(program_file):
    program = open(program_file,'r')
    lines=program.read().splitlines()
    program.close()
    return lines
    
def compile_lines(lines,labels,var,e=False):
    obj_str=""
    if e : 
        labels_hex = dict.copy(labels)
        for lab in labels : labels_hex[lab] = '0x'+format(labels[lab],'x').zfill(2)
        gpr_var   = [v for v in var if v not in set(SFR) ]
        variables = dict(zip(gpr_var, [(var[v]-12,'0x'+format(var[v],'x').zfill(2)) for v in gpr_var]))
        print(green+'Compiled program : ')
        print(yellow+'GPR variables :'+blue,variables,black)
        print(yellow+'labels        :'+blue,labels_hex)
        print(yellow+'addr  '+'instruction'.ljust(20)+'opcode operand   hex_instr'+black)
    for instr_str,l in zip(lines,range(len(lines))):
        if instr_str == 'END' : break
        instr_bin = encode_instr(instr_str,labels,var)
        instr_hex = format(int(instr_bin,2),'x').zfill(4);
        if e : print(blue+('0x'+format(l,'x').zfill(2)).ljust(6)+red+instr_str.ljust(20) + green+instr_bin[:6]+' '+instr_bin[6:] + '  '+magenta+instr_hex+black)
        obj_str += instr_hex+"\n"
    return obj_str
    
def write_out(program_file,obj_str) : 
    folder = os.path.dirname(os.path.realpath(program_file))
    obj_file = folder+'/bin/'+os.path.basename(program_file).replace('.pic','.out')
    obj = open(obj_file,"w")
    obj.write("v2.0 raw\n")
    obj.write(obj_str)
    obj.close()
    print(green+"compilation sucess. binary file in :\n"+yellow+'%s' %(obj_file)+black)
    return obj_file

#### def : misc 
def bin_s(x,fill=8):
    return format(int(x),'b').zfill(fill)

##################################################################
###### run 
if __name__== '__main__':
    args=sys.argv
    if len(args) > 1: 
        program_file = args[1]
        verbose = '-v' in args or '--verbose' in args
        encode  = '-e' in args or '--encode' in args
    else : 
        program_file = PIC_folder+'/dat/test.apl'
    obj_file=compile_program(program_file,v=verbose,e=encode)