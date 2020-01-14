'''
This module generates 
    dat/PROM     : The PROM image as used in APPOLO.circ
    dat/PROM.pkl : All information about the data structure in PROM. To import do : 
df_PROM=pd.read_pickle('dat/PROM.pkl')
Notes : 
    It may need to be changed if the architecture is modified or extended 
'''

import pandas as pd
import numpy as np
import os,string    
from glob_colors import*
appolo_folder=os.path.dirname(__file__)


################################################################################
#                    This is where the PROM entries are defined 
################################################################################
#dat_sel : 0=data, 1=register, 2=input
#alu_sel : 0=bus_out, 1=add_bus_w, 2=cmp_bus
seq=2       #clock cycles for 1 instructions
instruction_bits = {
########### data_sel,   out_w,   acc_w,    sw_w,   reg_w, jmp0    , jmpIF  , alu_sel,
'JUMP'   : ['0'*seq , '0'*seq, '0'*seq, '0'*seq, '0'*seq, '10'    , '0'*seq, '0'*seq,] ,
'JUMPZ'  : ['0'*seq , '0'*seq, '0'*seq, '0'*seq, '0'*seq, '0'*seq , '10'   , '0'*seq,] ,
'LOADWL' : ['0'*seq , '0'*seq, '01'   , '0'*seq, '0'*seq, '0'*seq , '0'*seq, '0'*seq,] ,
'LOADWR' : ['1'*seq , '0'*seq, '01'   , '0'*seq, '0'*seq, '0'*seq , '0'*seq, '0'*seq,] ,
'LOADRW' : ['1'*seq , '0'*seq, '0'*seq, '0'*seq, '01'   , '0'*seq , '0'*seq, '0'*seq,] ,
'ADDWR'  : ['1'*seq , '0'*seq, '01'   , '01'   , '0'*seq, '0'*seq , '0'*seq, '10'   ,] ,
'ADDWL'  : ['0'*seq , '0'*seq, '01'   , '01'   , '0'*seq, '0'*seq , '0'*seq, '10'   ,] ,
'IN'     : ['2'*seq , '0'*seq, '01'   , '0'*seq, '0'*seq, '0'*seq , '0'*seq, '0'*seq,] ,
'OUT'    : ['0'*seq , '10'   , '0'*seq, '0'*seq, '0'*seq, '0'*seq , '0'*seq, '0'*seq,] ,
}
signal_bits = ['data_sel','out_w','acc_w','sw_w','reg_w','jmp0','jmpIF','alu_sel']
instruction_set = instruction_bits.keys()

#### get the hex code for the sequencer for each instruction
hex_codes = dict.fromkeys(instruction_set)#,[[]]*9))
for instr in instruction_set : 
    hex_codes[instr] = [];    #print(red+instr+black)
    for i in range(seq):
        bin_code = ''.join([format(int(bit[i]),'b') for bit in instruction_bits[instr]])
        hex_code =  hex(int(bin_code,2))[2:].zfill(3); #print(hex_code)
        hex_codes[instr] += [hex_code]
hex_codes = list(hex_codes.values())


#### save PROM
hex_codes_str = ''.join([' '.join(h)+'\n'  for h in hex_codes])
PROM_file = appolo_folder+'/dat/PROM'
obj = open(PROM_file,"w");
obj.write("v2.0 raw\n")
obj.write(hex_codes_str)
obj.close();
print('PROM saved:\n'+green+PROM_file+black)


#### create the dataframe containing all infos
df_PROM = pd.DataFrame(columns=['instruction','opcode']+signal_bits+['hex_codes'])
df_PROM['instruction']=instruction_set
df_PROM['opcode']=[s for s in string.hexdigits[:len(instruction_set)]]
df_PROM[signal_bits]=list(instruction_bits.values())
df_PROM['hex_codes']=hex_codes
df_PROM = df_PROM.set_index('instruction')
# save to pickle
PROM_pkl=appolo_folder+'/dat/PROM.pkl'
df_PROM.to_pickle(appolo_folder+'/dat/PROM.pkl')
print('pickle saved:\n'+green+appolo_folder+'/dat/PROM.pkl'+black)
