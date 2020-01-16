#!/usr/bin/python3

import sys 

def decode_instr(instr_hex):
    print(instr_hex)
    instr_bin = format(int(instr_hex,16),'b').zfill(26);print(instr_bin)
    dat       = instr_bin[-8:];#print(dat)
    st        = instr_bin[-11:-8]
    w         = instr_bin[-19:-11]
    opcode    = instr_bin[-25:-19]
    op7       = instr_bin[-25]
    str = """
dat     : %d
st      : %s
w       : %d
opcode  : %s
op7     : %s
    """  %(int(dat,2),st,int(w,2),opcode,op7)
    print(str)  
    
def decode_result(result_hex):
    print(result_hex)
    result_bin = format(int(result_hex,16),'b').zfill(15);print(result_bin)
    call_goto = result_bin[-2:];#print(dat)
    out       = result_bin[-10:-2]
    control   = result_bin[-11:-10]
    skip      = result_bin[-12:-11]
    status    = result_bin[-15:-12]
    str = """
call_goto : %s
out       : %d
control   : %s
skip      : %s
st        : %s
    """  %(call_goto, int(out,2), control, skip, status)
    print(str)     

func = {'r':decode_result,'i':decode_instr}[sys.argv[1]]
hex = sys.argv[2]
func(hex)    
