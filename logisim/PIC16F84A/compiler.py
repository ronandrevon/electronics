#! /usr/bin/python3
'''
Compiles a .pic text file and produces a .out binary file

    EXAMPLE : 
./compiler.py prog.pic -o prog_test.out -v -e

./compiler.py *prog*.pic [-o *outfile*] [-e or --encode]  [-v or --verbose]
    OPTIONS : 
-o : specify the output file in *outfile*
-e : show encoded information report 
-v : additional info

   Instruction types in .pic files : 
byte     : op(str) address(<80) d(boolean)
bit      : op(str) address(<80) bit(<8)
jump     : op(str) address(<1024)
literal  : op(str) data(<255)
control  : op(str)
'''

import numpy as np
import pandas as pd
from glob_colors import*
import os,sys

PIC_folder=os.path.dirname(__file__)
df_PROM=pd.read_pickle(PIC_folder+'/dat/PROM.pkl')
instruction_type = df_PROM['type']
opcode  = df_PROM['opcode']
SFR     = ['INDF','TMR0','OPTION','PCL','STATUS','FSR','PORTA','TRISA','PORTB','TRISB','EEDATA','EECON1','EEADR','EECON2','PCLATH','INTCON']

#### def : main program
def compile_program(program_file,v=False,e=False,o=None) : 
    ''' obj_file = compile_program('file.pic')'''
    lines           = load_program(program_file)
    lines,lab,var   = preprocess_lines(lines,verbose)
    obj_str         = compile_lines(lines,lab,var,e)
    obj_file        = write_out(program_file,obj_str,obj_file=o)
    return obj_file

''' Preprocessing stage '''
def preprocess_lines(lines,verbose=False) : 
    var_dict = dict(zip(['INDF','PCL','STATUS','FSR','PCLATH','INTCON'],[0,2,3,4,10,11]))
    var_dict.update(dict(zip(['TMR0'  ,'TRISA','TRISB','EECON1','EECON2'],[1,5,6,8,9])))
    var_dict.update(dict(zip(['OPTION','PORTA','PORTB','EEDATA','EEADR' ],[1,5,6,8,9])))
    lines = [line.split("#")[0] for line in lines] # remove comments
    lines = [line for line in lines if line] # remove empty lines
    instructions_dat = []
    ## check for variable from the end of the file 
    var,line,lc,lv = dict(),lines[-1],len(lines)-1,12
    while "=" in line : 
        var_name,vals   = line.split("=")
        vals            = vals.split(',');nv=len(vals)
        if 'x' in vals[0] : vals=[str(int(v[1:],16)) for v in vals ] #handle hexadecimal parsing for ascii
        var[var_name]   = lv
        instructions_dat    += ['MOVLW ' +vals[0].replace('  ',''), 'MOVWF '+var_name]
        # if the variable is an array
        for i in range(1,nv) : 
            var[var_name+str(i)] = lv+i
            instructions_dat += ['MOVLW ' +vals[i].replace('  ',''), 'MOVWF '+var_name+str(i)];
        lv+=nv
        lc-=1;line=lines[lc];
    lines = lines[:lc+1]
    var_dict.update(var)
    if verbose : 
        print(green+'   data section : '+black)
        print(yellow+'variables : '+blue,var,black)
        print(red+'\n'.join(map(lambda a,b:str(a)+' '+b,range(len(instructions_dat)),instructions_dat))+black)
    
    ## preprocess program text
    instructions,li, labels, var_tmp = [],0, dict(), []
    for line in lines : 
        ## check for labels
        line = line.split(":")
        if len(line)>1 : 
            lab,instr = line
        else : 
            lab,instr = '',line[0]
        #get instruction type
        op = instr.split(" ")[0]
        if op in df_PROM.index : 
            if lab : labels[lab] = li
            instructions.append(instr.replace('  ',''));li+=1
            if instruction_type[op] in ['byte','bit','mem'] : 
                var_tmp.append( instr.split(" ")[1])
    # resolve address of variables created on the fly
    var_tmp = [v for v in np.unique(var_tmp) if v not in var_dict.keys()]
    var_tmp = dict(zip(var_tmp, np.arange(len(var_tmp))+lv))
    if verbose : 
        print(green+'   text section : ')
        print(yellow+'labels:'+blue,labels)
        print(yellow+'variables:'+blue,var_tmp,black)
        print(yellow+'instructions : '+red,np.unique([i.split(' ')[0] for i in instructions]),black)
        print(red+'\n'.join(map(lambda a,b:str(a)+' '+b,range(len(instructions)),instructions))+black);
    var_dict.update(var_tmp)
    if 'init' in labels.keys() : instructions_dat += ['GOTO init']
    instructions+=instructions_dat
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
        if k in var.keys() : k=var[k]     # allowing variable addresses to be parsed as literal
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
        print(green+'\n    Compiled program : ')
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
    
def write_out(program_file,obj_str,obj_file=None) : 
    folder = os.path.dirname(os.path.realpath(program_file))
    if not obj_file : obj_file = folder+'/bin/'+os.path.basename(program_file).replace('.pic','.out')
    obj = open(obj_file,"w")
    obj.write("v2.0 raw\n")
    obj.write(obj_str)
    obj.close()
    print(green+"compilation sucess. binary file in :\n"+yellow+'%s' %(obj_file)+black)
    return obj_file

#### def : misc 
def bin_s(x,fill=8):
    ''' convert integer into filled binary string'''
    return format(int(x),'b').zfill(fill)

##################################################################
###### run 
if __name__== '__main__':
    args=sys.argv;
    if len(args) > 1: 
        program_file = args[1]
        verbose  = '-v' in args or '--verbose' in args
        encode   = '-e' in args or '--encode' in args
        outfile  = '-o' in args or '--outfile' in args
    obj_file=''
    if outfile : obj_file = args[(np.array(args)=='-o').argmax() + 1]
    obj_file=compile_program(program_file,v=verbose,e=encode,o=obj_file)