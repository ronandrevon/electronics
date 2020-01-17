# PIC16F84A

1. [features](#features)
1. [Getting started](#getting-started)
1. [Instruction set](#instruction-set)
1. [Folders and files structure](#folders-and-files-structure)

## Features

General features : 

- 35 instruction set
- 1024 instructions of program memory each 14 bit wide
- 68x8 bit General purpose registers
- 13 I/O ports : RA0-RA4 and RB0-RB7

Special features : 

- 4 Interruption sources (interrupt vector 004) on : 
    - external asynchronous on port **RB0/INT**
    - change on ports **RB4:RB7**
    - timer **TMR0** time out
    - data **EEPROM** write complete
- Function calls and return from interrupt through 8 level **stack**
- Indirect addresssing mode through the File Select Register (**FSR**) which is essentially a pointer
- 15 hardware Special Function Registers (**SFR**) addressing 
    - PCL/PCLATH, STATUS, FSR, INTCON
    - TIMR0,  PORTA, PORTB, EEADR,  EEDATA
    - OPTION, TRISA, TRISB, EECON1, EECON2
- PCL/PCLATH jump addressing (for virtual functions)
- **EEPROM** access (variable read/write access time)
- SLEEP mode and watchdog timer(**WDT**) to resume


BUS : 
- There should always be a value on the BUS but even when not used
- There cannot be any conflct on bus since only memory registers are allowed on it and a single address is used in the RAM 

Special registers : 
- Accessible for R/W independently from the BUS 
- READ  : PCL,PCLATH,TIMR0,STATUS,FSR, INTCON, EECON1,EEADDR, PORTA,TRISA
- WRITE : STATUS,INTCON, EEDATA,EECON1

SFR configuration
STATUS config : 
Read Status  => ST addresss, RAM-Q on BUS 
Write Status => ST address(direct or indirect), STATUS on BUS 
->Carry ou ALU => D in Buffer, Buffer Q on BUS,ST address Mult-in, 
->Carry in ALU => Buffer Q on BUS, ST address Mult-in 

INTCON config : 
Asynchronous interrupt : 


## Getting started

The simulator can be lauchned with : 

    logisim PIC16F84A.circ &
A program can be written in an assembler ***file*.pic** file (see 
[Instruction set](#instruction-set) to learn this basic language and 
[test.pic](#) to see an test example).
The programs can be compiled using the compiler *compiler.py* written in
python3. For example the test program would be compiled with : 

    ./compiler.py programs/test.pic -e -v
where 
- -e : option to display encoded information (highly recommended)
- -v : verbose option

A binary file **bin/test.out** has been produced. Then :
- load the binary file **programs/bin/test.out** into the **program RAM memory** of the Apollo simulator.
- The execution can be started using **START** button.
- The 4 **inputs** can be modified at will.
- The **RESET** button can be used at anytime to reset the CPU to original state.
- Use **Ctrl+E** to enable the clock to tick.
- Use **Ctrl+K** to start ticking.
- Use **Ctrl+T** to tick one at a time
- Monitor the state of each aspects of the CPU through the probes of the *Monitoring* panel. In particular, the output of the computation can be seen in the *MEMORY/Outputs* tab.

![RAM](file:///home/ronan/Documents/github/electronics/logisim/PIC16F84A/doc/PIC16F84A.png)



## Instruction set


instruction|operand|opcode|description|status
-----------|-      |-----|-----------|------
**Byte Oriented**
ADDWF   |f,d| 00 0111|Add W and f|CDZ
ANDWF   |f,d| 00 0101|AND W with f|Z
CLRF    |f  | 00 0001|Clear f|Z
CLRW    | - | 00 0001|Clear W|Z
COMF    |f,d| 00 1001|Complement f|Z
DECF    |f,d| 00 0011|Decrement f|Z
DECFSZ  |f,d| 00 1011|Decrement f, Skip if 0|Z
INCF    |f,d| 00 1010|Increment f|
INCFSZ  |f,d| 00 1111|Increment f, Skip if 0|
IORWF   |f,d| 00 0100|Inclusive OR W with f|Z
MOVF    |f,d| 00 1000|Move f|Z
MOVWF   |f  | 00 0000|Move W to f|
NOP     | - | 00 0000|No Operation|
RLF     |f,d| 00 1101|Rotate Left f through Carry|C
RRF     |f,d| 00 1100|Rotate Right f through Carry|C
SUBWF   |f,d| 000010|Subtract W from f|CDZ
SWAPF   |f,d| 001110|Swap nibbles in f|
XORWF   |f,d| 000110|Exclusive OR W with f|Z
**Bit oriented**
BCF     |f,b| 01 00|Bit Clear f|
BSF     |f,b| 01 01|Bit Set f|
BTFSC   |f,b| 01 10|Bit Test f, Skip if Clear|
BTFSS   |f,b| 01 11|Bit Test f, Skip if Set|
**Litteral oriented and control**
ADDLW   |k  | 11 1110|Add literal and W|CDZ
ANDLW   |k  | 11 1001|AND literal with W|Z
CALL    |k  | 10 0000|Call subroutine|
CLRWDT  | - | 00 0000|Clear Watchdog Timer|TP
GOTO    |k  | 10 1000|Go to address|
IORLW   |k  | 11 1000|Inclusive OR literal with W|Z
MOVLW   |k  | 11 0000|Move literal to W|
RETFIE  | - | 00 0000|Return from interrupt|
RETLW   |k  | 11 0100|Return with literal in W|
RETURN  | - | 00 0000|Return from Subroutine|
SLEEP   | - | 00 0000|Go into standby mode|TP
SUBLW   |k  | 11 1100|Subtract W from literal|CDZ
XORLW   |k  | 11 1010|Exclusive OR literal with W|Z


  - **decode_hex.py**  : decode heaxdecimal instruction into human readable ascii instruction 
  - **cmp_results.py** : compares results from out and expected output