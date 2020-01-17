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
PIC_folder=os.path.dirname(__file__)

################################################################################
#                    This is where the PROM entries are defined 
################################################################################
seq=4       #number of clock cycles for one instructions
signals = [   'push'  ,'pop'  ,'jmp'  ,'skip_e','RAM_r','result_w','sw_w' ,'reg_w','clrwdt','sleep']
instruction_bits = {
# Byte oriented 
'ADDWF'     : ['0'*seq,'0'*seq,'0'*seq,'0'*seq ,'1100' ,'0'*seq   ,'0'*seq,'0'*seq,'0'*seq,'0'*seq,],
'ANDWF'     : ['0'*seq,'0'*seq,'0'*seq,'0'*seq ,'1100' ,'0'*seq   ,'0'*seq,'0'*seq,'0'*seq,'0'*seq,],
'CLRF'      : ['0'*seq,'0'*seq,'0'*seq,'0'*seq ,'1100' ,'0'*seq   ,'0'*seq,'0'*seq,'0'*seq,'0'*seq,],
'CLRW'      : ['0'*seq,'0'*seq,'0'*seq,'0'*seq ,'1100' ,'0'*seq   ,'0'*seq,'0'*seq,'0'*seq,'0'*seq,],
'COMF'      : ['0'*seq,'0'*seq,'0'*seq,'0'*seq ,'1100' ,'0'*seq   ,'0'*seq,'0'*seq,'0'*seq,'0'*seq,],
'DECF'      : ['0'*seq,'0'*seq,'0'*seq,'0'*seq ,'1100' ,'0'*seq   ,'0'*seq,'0'*seq,'0'*seq,'0'*seq,],
'DECFSZ'    : ['0'*seq,'0'*seq,'0'*seq,'0'*seq ,'1100' ,'0'*seq   ,'0'*seq,'0'*seq,'0'*seq,'0'*seq,],
'INCF'      : ['0'*seq,'0'*seq,'0'*seq,'0'*seq ,'1100' ,'0'*seq   ,'0'*seq,'0'*seq,'0'*seq,'0'*seq,],
'INCFSZ'    : ['0'*seq,'0'*seq,'0'*seq,'0'*seq ,'1100' ,'0'*seq   ,'0'*seq,'0'*seq,'0'*seq,'0'*seq,],
'IORWF'     : ['0'*seq,'0'*seq,'0'*seq,'0'*seq ,'1100' ,'0'*seq   ,'0'*seq,'0'*seq,'0'*seq,'0'*seq,],
'MOVF'      : ['0'*seq,'0'*seq,'0'*seq,'0'*seq ,'1100' ,'0'*seq   ,'0'*seq,'0'*seq,'0'*seq,'0'*seq,],
'MOVWF'     : ['0'*seq,'0'*seq,'0'*seq,'0'*seq ,'1100' ,'0'*seq   ,'0'*seq,'0'*seq,'0'*seq,'0'*seq,],
'NOP'       : ['0'*seq,'0'*seq,'0'*seq,'0'*seq ,'1100' ,'0'*seq   ,'0'*seq,'0'*seq,'0'*seq,'0'*seq,],
'RLF'       : ['0'*seq,'0'*seq,'0'*seq,'0'*seq ,'1100' ,'0'*seq   ,'0'*seq,'0'*seq,'0'*seq,'0'*seq,],
'RRF'       : ['0'*seq,'0'*seq,'0'*seq,'0'*seq ,'1100' ,'0'*seq   ,'0'*seq,'0'*seq,'0'*seq,'0'*seq,],
'SUBWF'     : ['0'*seq,'0'*seq,'0'*seq,'0'*seq ,'1100' ,'0'*seq   ,'0'*seq,'0'*seq,'0'*seq,'0'*seq,],
'SWAPF'     : ['0'*seq,'0'*seq,'0'*seq,'0'*seq ,'1100' ,'0'*seq   ,'0'*seq,'0'*seq,'0'*seq,'0'*seq,],
'XORWF'     : ['0'*seq,'0'*seq,'0'*seq,'0'*seq ,'1100' ,'0'*seq   ,'0'*seq,'0'*seq,'0'*seq,'0'*seq,],
# Bit oriented
'BCF'       : ['0'*seq,'0'*seq,'0'*seq,'0'*seq ,'1100' ,'0'*seq   ,'0'*seq,'0'*seq,'0'*seq,'0'*seq,],
'BSF'       : ['0'*seq,'0'*seq,'0'*seq,'0'*seq ,'1100' ,'0'*seq   ,'0'*seq,'0'*seq,'0'*seq,'0'*seq,],
'BTFSC'     : ['0'*seq,'0'*seq,'0'*seq,'0'*seq ,'1100' ,'0'*seq   ,'0'*seq,'0'*seq,'0'*seq,'0'*seq,],
'BTFSS'     : ['0'*seq,'0'*seq,'0'*seq,'0'*seq ,'1100' ,'0'*seq   ,'0'*seq,'0'*seq,'0'*seq,'0'*seq,],
#Litteral/control
'ADDLW'     : ['0'*seq,'0'*seq,'0'*seq,'0'*seq ,'0'*seq,'0'*seq   ,'0'*seq,'0'*seq,'0'*seq,'0'*seq,],
'ANDLW'     : ['0'*seq,'0'*seq,'0'*seq,'0'*seq ,'0'*seq,'0'*seq   ,'0'*seq,'0'*seq,'0'*seq,'0'*seq,],
'CALL'      : ['0100' ,'0'*seq,'0010' ,'0'*seq ,'0'*seq,'0'*seq   ,'0'*seq,'0'*seq,'0'*seq,'0'*seq,],
'CLRWDT'    : ['0'*seq,'0'*seq,'0'*seq,'0'*seq ,'0'*seq,'0'*seq   ,'0'*seq,'0'*seq,'0100' ,'0'*seq,],
'GOTO'      : ['0'*seq,'0'*seq,'0010' ,'0'*seq ,'0'*seq,'0'*seq   ,'0'*seq,'0'*seq,'0'*seq,'0'*seq,],
'IORLW'     : ['0'*seq,'0'*seq,'0'*seq,'0'*seq ,'0'*seq,'0'*seq   ,'0'*seq,'0'*seq,'0'*seq,'0'*seq,],
'MOVLW'     : ['0'*seq,'0'*seq,'0'*seq,'0'*seq ,'0'*seq,'0'*seq   ,'0'*seq,'0'*seq,'0'*seq,'0'*seq,],
'RETFIE'    : ['0'*seq,'0100' ,'0010' ,'0'*seq ,'0'*seq,'0'*seq   ,'0'*seq,'0'*seq,'0'*seq,'0'*seq,],
'RETLW'     : ['0'*seq,'0100' ,'0010' ,'0'*seq ,'0'*seq,'0'*seq   ,'0'*seq,'0'*seq,'0'*seq,'0'*seq,],
'RETURN'    : ['0'*seq,'0100' ,'0010' ,'0'*seq ,'0'*seq,'0'*seq   ,'0'*seq,'0'*seq,'0'*seq,'0'*seq,],
'SLEEP'     : ['0'*seq,'0'*seq,'0'*seq,'0'*seq ,'0'*seq,'0'*seq   ,'0'*seq,'0'*seq,'0'*seq,'0100' ,],
'SUBLW'     : ['0'*seq,'0'*seq,'0'*seq,'0'*seq ,'0'*seq,'0'*seq   ,'0'*seq,'0'*seq,'0'*seq,'0'*seq,],
'XORLW'     : ['0'*seq,'0'*seq,'0'*seq,'0'*seq ,'0'*seq,'0'*seq   ,'0'*seq,'0'*seq,'0'*seq,'0'*seq,],
}
descriptions = [
'Add W and f','AND W with f','Clear f','Clear W','Complement f','Decrement f','Decrement f, Skip if 0','Increment f','Increment f, Skip if 0','Inclusive OR W with f','Move f','Move W to f','No Operation','Rotate Left f through Carry','Rotate Right f through Carry','Subtract W from f','Swap nibbles in f','Exclusive OR W with f',
'Bit Clear f','Bit Set f','Bit Test f, Skip if Clear','Bit Test f, Skip if Set',
'Add literal and W','AND literal with W','Call subroutine','Clear Watchdog Timer','Go to address','Inclusive OR literal with W','Move literal to W','Return from interrupt','Return with literal in W','Return from Subroutine','Go into standby mode','Subtract W from literal','Exclusive OR literal with W',
]
op_codes = [
'000111','000101','000001','000001','001001','000011','001011','001010','001111','000100','001000','000000','000000','001101','001100','000010','001110','000110',
'0100','0101','0110','0111',
'111110','111001','100000','000000','101000','111000','110000','000000','110100','000000','000000','111100','111010'
]
instruction_types = ['byte']*18 + ['bit']*4 + ['litteral','litteral','jump','control','jump','litteral','litteral','control','litteral','control','control','litteral','litteral']
status_affected = ['CDZ']+['Z']*5+['Z','','','Z','Z','','','C','C','CDZ','','Z']+['']*4+['CDZ','Z','','TP','','Z']+['']*4+['TP','CDZ','Z']
instruction_set = instruction_bits.keys()


#################################################################################
#                     Write PROM and PROM.pkl(Should not need to change)      
#################################################################################
#### get the hex codes for the sequencer for each instruction
hex_codes,nbits = dict.fromkeys(instruction_set),int(np.ceil(np.log2(len(signals))))
for instr in instruction_set : 
    hex_codes[instr] = [];   print(red+instr+black)
    for i in range(seq):
        bin_code = ''.join([val[i] for val in instruction_bits[instr]])
        hex_code =  hex(int(bin_code,2))[2:].zfill(nbits); print(bin_code,hex_code)
        hex_codes[instr] += [hex_code]
hex_codes = list(hex_codes.values())

#### save PROM
hex_codes_str = ''.join([' '.join(h)+'\n'  for h in hex_codes])
PROM_file = PIC_folder+'/dat/PROM'
obj = open(PROM_file,"w");
obj.write("v2.0 raw\n")
obj.write(hex_codes_str)
obj.close();
print('PROM saved:\n'+green+PROM_file+black)


#### create the dataframe containing all infos
df_PROM = pd.DataFrame(columns=['instruction','description','opcode','type','status','hex_codes']+signals)
df_PROM['instruction']  = instruction_set
df_PROM['description']  = descriptions
df_PROM['opcode']       = op_codes
df_PROM['type']         = instruction_types
df_PROM['status']       = status_affected
df_PROM[signals]        = list(instruction_bits.values())
df_PROM['hex_codes']    = hex_codes
df_PROM = df_PROM.set_index('instruction')
# save to pickle
PROM_pkl=PIC_folder+'/dat/PROM.pkl'
df_PROM.to_pickle(PIC_folder+'/dat/PROM.pkl')
print('pickle saved:\n'+green+PIC_folder+'/dat/PROM.pkl'+black)

#df_PROM[['opcode','description','status']].to_csv('dat/PROM.csv',sep='|')