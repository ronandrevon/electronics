#! /bin/bash
#./flash_PIC.sh *PROGRAM* [-d || --diff]
#
#   Description : 
# Inject the program *PROGRAM* in the Flash ROM of the PIC 
# The resulting circuit is put in dat/tests/PIC_tmp.circ
#   OPTION : 
# -d : display differences between the oiginal and output circuit

PROGRAM=$1
diff=0; if [ $# -eq 2 ]; then if [ $2 == "-d" ] || [ $2 == "--diff" ]; then diff=1; fi; fi; #;echo $diff

base=$(realpath `dirname $0`/..)        # This file is currently located in /programs
CIRCUIT=$base/PIC16F84A.circ            # Original circuit 
TMP_CIRC=$base/dat/tests/PIC16F84A.circ # Output circuit
ROM_pattern="data: 13 14"               # Pattern to identify location of the Flash ROM 


#remove existing ROM lines and put circuit in PIC_tmp.circ
sed "/$ROM_pattern/,/</{s/^[0-9 a-f]*$//; t;}" $CIRCUIT > $TMP_CIRC

#fetch program
prog=$(sed -n '2,$p' $PROGRAM | tr '\n' ' ')                            #;printf "$prog\n"

# inject in temporary circuit file
sed -i "/$ROM_pattern/a $prog" $TMP_CIRC


#Output differences
if [ $diff -eq 1 ]; then diff --color $CIRCUIT $TMP_CIRC; fi