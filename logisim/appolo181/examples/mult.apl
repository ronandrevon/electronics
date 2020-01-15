#### PROGRAM multiply(a,b)
#initialize registers 
IN 0
LOADRW 0    # R0 : multiple to be added each time
IN 1
LOADRW 1    # R1 : mutiplicand
LOADWL 0
LOADRW 2    # R2 : result
LOADRW 3    # R3 : counter
# compare counter R3 with mutiplicand R1
loop:LOADWR 3
CMPWR 1
# if equal jump at the end of the loop
JUMPZ out
# else increment result R2 with R0
LOADWR 2
ADDWR 0
LOADRW 2
# increment counter R3
LOADWR 3
ADDWL 1
LOADRW 3
#loop back
JUMP loop
#Output result R2 into output O0
out:LOADWR 2
OUT 0
END


#### python equivalent
def mult(a,b):
    c=0
    for i in range(a):
        c+=b
    return c
mult(1,2)
