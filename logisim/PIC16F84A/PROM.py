#! /usr/bin/python3
'''
This module generates 
    dat/PROM     : The PROM image as used in PIC16F84A.circ
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

#################################################################################
#                          Instruction set                                     
#################################################################################
seq = 4  #number of clock cycles for one instructions
signals = ['push' ,'pop'   ,'call'  ,'skip_e','result_w','sw_w' ,'reg_w' ,'clrwdt','sleep']
instruction_set = [
'ADDWF','ANDWF','CLRF','CLRW','COMF','DECF','DECFSZ','INCF','INCFSZ','IORWF','MOVF','MOVWF','NOP','RLF','RRF','SUBWF','SWAPF','XORWF',
'BCF','BSF','BTFSC','BTFSS',
'ADDLW','ANDLW','CALL','CLRWDT','GOTO','IORLW','MOVLW','RETFIE','RETLW','RETURN','SLEEP','SUBLW','XORLW',
]
op_codes = [
'000111','000101','0000011','000001'+'0'*8,'001001','000011','001011','001010','001111','000100','001000','0000001','0'*14,'001101','001100','000010','001110','000110',
'0100','0101','0110','0111',
'111110','111001','100','00000001100100','101','111000','110000','00000000001001','110100','0'*10+'1000','00000001100011','111100','111010'
]
descriptions = [
'Add W and f','AND W with f','Clear f','Clear W','Complement f','Decrement f','Decrement f, Skip if 0','Increment f','Increment f, Skip if 0','Inclusive OR W with f','Move f','Move W to f','No Operation','Rotate Left f through Carry','Rotate Right f through Carry','Subtract W from f','Swap nibbles in f','Exclusive OR W with f',
'Bit Clear f','Bit Set f','Bit Test f, Skip if Clear','Bit Test f, Skip if Set',
'Add literal and W','AND literal with W','Call subroutine','Clear Watchdog Timer','Go to address','Inclusive OR literal with W','Move literal to W','Return from interrupt','Return with literal in W','Return from Subroutine','Go into standby mode','Subtract W from literal','Exclusive OR literal with W',
]
instruction_types   = ['byte']*2 + ['mem','control'] + ['byte']*7 + ['mem','control'] +['byte']*5 + ['bit']*4 + ['litteral','litteral','jump','control','jump','litteral','litteral','control','litteral','control','control','litteral','litteral']
status_affected     = ['CDZ']+['Z']*5+['Z','','','Z','Z','','','C','C','CDZ','','Z']+['']*4+['CDZ','Z','','TP','','Z']+['']*4+['TP','CDZ','Z']

def get_hex_codes(instruction_set,instruction_bits,seq) : 
    hex_codes,nbits = dict.fromkeys(instruction_set),int(np.ceil(np.log2(len(signals))))
    for instr in instruction_set : 
        hex_codes[instr] = [];   print(red+instr+black)
        for i in range(seq):
            bin_code = ''.join([val[i] for val in instruction_bits.loc[instr]])
            hex_code =  hex(int(bin_code,2))[2:].zfill(nbits); print(bin_code,hex_code)
            hex_codes[instr] += [hex_code]
    hex_codes = list(hex_codes.values())
    return hex_codes

#### create the dataframe containing all infos
df_PROM = pd.DataFrame(columns=['instruction','description','opcode','type','status','hex_codes']+signals)
df_PROM['instruction']  = instruction_set
df_PROM['description']  = descriptions
df_PROM['opcode']       = op_codes
df_PROM['type']         = instruction_types
df_PROM['status']       = status_affected
df_PROM[signals]        = ['0'*seq]*len(signals)
df_PROM = df_PROM.set_index('instruction')

#################################################################################
#                          PROM signals                                     
#################################################################################
# specific sequences 
byte_type,mem_type,bit_type,litt_type,control_type,jump_type = df_PROM['type']=='byte', df_PROM['type']=='mem',df_PROM['type']=='bit', df_PROM['type']=='litteral', df_PROM['type']=='control', df_PROM['type']=='jump'
r_type = byte_type | mem_type | bit_type | litt_type
df_PROM['result_w'].loc[r_type] = '0100'

hex_codes = get_hex_codes(df_PROM.index,df_PROM[signals],seq)
df_PROM['hex_codes'] = hex_codes

#### save PROM
hex_codes_str = ''.join([' '.join(h)+'\n'  for h in hex_codes])
PROM_file = PIC_folder+'/dat/PROM'
obj = open(PROM_file,"w");
obj.write("v2.0 raw\n")
obj.write(hex_codes_str)
obj.close();
print('PROM saved:\n'+green+PROM_file+black)

# save to pickle
PROM_pkl=PIC_folder+'/dat/PROM.pkl'
df_PROM.to_pickle(PIC_folder+'/dat/PROM.pkl')
print('pickle saved:\n'+green+PIC_folder+'/dat/PROM.pkl'+black)

#df_PROM[['opcode','description','status']].to_csv('dat/PROM.csv',sep='|')