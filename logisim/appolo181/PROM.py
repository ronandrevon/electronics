#! /usr/bin/python3
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
#dat_sel : 0=input, 1=data, 2=register
#alu_sel : 0=bus_out/cmp, 1=add_bus_w
seq=2       #number of clock cycles for 1 instructions
instruction_bits = {
########### data_sel,   out_w,   acc_w,    sw_w,   reg_w, jmp0    , jmpIF  , alu_sel,
'NOPE'   : ['1'*seq , '0'*seq, '0'*seq, '0'*seq, '0'*seq, '0'*seq , '0'*seq, '0'*seq,] ,
'JUMP'   : ['1'*seq , '0'*seq, '0'*seq, '0'*seq, '0'*seq, '10'    , '0'*seq, '0'*seq,] ,
'JUMPZ'  : ['1'*seq , '0'*seq, '0'*seq, '0'*seq, '0'*seq, '0'*seq , '10'   , '0'*seq,] ,
'LOADRW' : ['2'*seq , '0'*seq, '0'*seq, '0'*seq, '01'   , '0'*seq , '0'*seq, '0'*seq,] ,
'LOADWR' : ['2'*seq , '0'*seq, '01'   , '0'*seq, '0'*seq, '0'*seq , '0'*seq, '0'*seq,] ,
'CMPWR'  : ['2'*seq , '0'*seq, '0'*seq, '01'   , '0'*seq, '0'*seq , '0'*seq, '0'*seq,] ,
'ADDWR'  : ['2'*seq , '0'*seq, '01'   , '01'   , '0'*seq, '0'*seq , '0'*seq, '11'   ,] ,
'LOADWL' : ['1'*seq , '0'*seq, '01'   , '0'*seq, '0'*seq, '0'*seq , '0'*seq, '0'*seq,] ,
'CMPWL'  : ['1'*seq , '0'*seq, '0'*seq, '01'   , '0'*seq, '0'*seq , '0'*seq, '0'*seq,] ,
'ADDWL'  : ['1'*seq , '0'*seq, '01'   , '01'   , '0'*seq, '0'*seq , '0'*seq, '11'   ,] ,
'IN'     : ['0'*seq , '0'*seq, '01'   , '0'*seq, '0'*seq, '0'*seq , '0'*seq, '0'*seq,] ,
'OUT'    : ['1'*seq , '10'   , '0'*seq, '0'*seq, '0'*seq, '0'*seq , '0'*seq, '0'*seq,] ,
}
descriptions = {
'NOPE'   : 'no operation', 
'JUMP'   : 'jump to location acc*16 + dat',
'JUMPZ'  : 'jump to location acc*16 + dat if status flag Z=1',
'LOADRW' : 'load register R=DAT with accumulator W',
'LOADWR' : 'load accumulator W with register R=DAT',
'CMPWR'  : 'Sets status flag Z=1 if accumulator W equals register R=DAT',
'ADDWR'  : 'Adds accumulator W with register R=DAT. Sets status flag C=1 if carry arises',
'LOADWL' : 'load accumulator W with litteral DAT',
'CMPWL'  : 'Sets status flag Z=1 if accumulator W equals litteral DAT',
'ADDWL'  : 'Adds accumulator W with litteral DAT. Sets status flag C=1 if carry arises',
'IN'     : 'Load accumulator W with input IN=DAT',
'OUT'    : 'Write to output OUT=DAT with accumulator W',
}

signal_bits = {'data_sel':2,'out_w':1,'acc_w':1,'sw_w':1,'reg_w':1,'jmp0':1,'jmpIF':1,'alu_sel':4}
signals,bits = list(signal_bits.keys()),list(signal_bits.values())
instruction_set = instruction_bits.keys()


#################################################################################
#                     Write PROM and PROM.pkl(Should not need to change)      
#################################################################################
#### get the hex codes for the sequencer for each instruction
hex_codes = dict.fromkeys(instruction_set)#,[[]]*9))
for instr in instruction_set : 
    hex_codes[instr] = [];   print(red+instr+black)
    for i in range(seq):
        bin_code = ''.join([format(int(val[i]),'b').zfill(nbits) for (val,nbits) in zip(instruction_bits[instr],bits)])
        hex_code =  hex(int(bin_code,2))[2:].zfill(3); print(bin_code,hex_code)
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
df_PROM = pd.DataFrame(columns=['instruction','opcode','hex_codes','description']+signals)
df_PROM['instruction']=instruction_set
df_PROM['opcode']=[s for s in string.hexdigits[:len(instruction_set)]]
df_PROM[signals]=list(instruction_bits.values())
df_PROM['hex_codes']=hex_codes
df_PROM['description']=descriptions.values()
df_PROM = df_PROM.set_index('instruction')
# save to pickle
PROM_pkl=appolo_folder+'/dat/PROM.pkl'
df_PROM.to_pickle(appolo_folder+'/dat/PROM.pkl')
print('pickle saved:\n'+green+appolo_folder+'/dat/PROM.pkl'+black)
