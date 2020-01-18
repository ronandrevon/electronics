# PIC16F84A

1. [Development](#development-status)
1. [features](#features)
1. [Getting started](#getting-started)
1. [Instruction set](#instruction-set)
1. [Folders and files structure](#folders-and-files-structure)

## Develpment status

- [ ] Complete PROM.py
- [ ] Update compiler.py
- [ ] **Memory** read and write access : MOVWF, MOVF, MOVLW / CLRF,CLRW #5
- [ ] **ALU** operations : NOP, ADDWF, ANDWF, COMF, DECF, INCF, IORWF, RLF, RRF, SUBWF, SWAPF, XORWF  /  BCF, BSF /  ADDLW, ANDLW, IORLW, SUBLW, XORLW #19
- [ ] **Call** functions + push : CALL, GOTO #2
- [ ] **Skip** operations : BTFSC, BTFSS, DECFSZ, INCFSZ #4
- [ ] **Return** from functions + pop : RETFIE, RETLW, RETURN #3
- [ ] **Sleep** mode : CLRWDT, SLEEP #2
- [ ] **Interrupts** : 
    - [ ] external asynchronous on port **RB0/INT**
    - [ ] change on ports **RB4:RB7**
    - [ ] timer **TMR0** time out
    - [ ] data **EEPROM** write complete

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

Each instruction is of the form : 

    label : INSTRUCTION [operand] #Some comment
where : 
- **label** is optionally used to refer to a specific location for jump instructions
- **INSRUCTION** must belong to the instruction set below
- **operand** depends on the instruction : 
    - **f** : an 7-bit memory address (between 0-80)
    - **d** : a destination boolean for the result (0=>W,1=>f)
    - **b** : a 3-bit number indicating the position of the bit being affected(between 0-7)
    - **k** : an 8-bit litteral number (between 0-255)
    - **a** : an 11-bit program address (between 0-1024)
- **\#** Anything after this character is a comment and therefore not compiled


instruction|opcode|operand|description|status
-----------|------|-------|-----------|------
NOP     | 00 000000000000| - |No Operation|
**Byte Oriented**
ADDWF   | 00 0111dfffffff|f,d|Add W and f|CDZ
ANDWF   | 00 0101dfffffff|f,d|AND W with f|Z
CLRF    | 00 00011fffffff|f  |Clear f|Z
CLRW    | 00 000100000000| - |Clear W|Z
COMF    | 00 1001dfffffff|f,d|Complement f|Z
DECF    | 00 0011dfffffff|f,d|Decrement f|Z
DECFSZ  | 00 1011dfffffff|f,d|Decrement f, Skip if 0|Z
INCF    | 00 1010dfffffff|f,d|Increment f|
INCFSZ  | 00 1111dfffffff|f,d|Increment f, Skip if 0|
IORWF   | 00 0100dfffffff|f,d|Inclusive OR W with f|Z
MOVF    | 00 1000dfffffff|f,d|Move f|Z
MOVWF   | 00 00001fffffff|f  |Move W to f|
RLF     | 00 1101dfffffff|f,d|Rotate Left f through Carry|C
RRF     | 00 1100dfffffff|f,d|Rotate Right f through Carry|C
SUBWF   | 00 0010dfffffff|f,d|Subtract W from f|CDZ
SWAPF   | 00 1110dfffffff|f,d|Swap nibbles in f|
XORWF   | 00 0110dfffffff|f,d|Exclusive OR W with f|Z
**Bit oriented**
BCF     | 01 00bbbfffffff|f,b|Bit Clear f|
BSF     | 01 01bbbfffffff|f,b|Bit Set f|
BTFSC   | 01 10bbbfffffff|f,b|Bit Test f, Skip if Clear|
BTFSS   | 01 11bbbfffffff|f,b|Bit Test f, Skip if Set|
**Litteral oriented and control**
ADDLW   | 11 1110kkkkkkkk|k  |Add literal and W|CDZ
ANDLW   | 11 1001kkkkkkkk|k  |AND literal with W|Z
CALL    | 10 0aaaaaaaaaaa|a  |Call subroutine|
CLRWDT  | 00 000001100100| - |Clear Watchdog Timer|TP
GOTO    | 10 1aaaaaaaaaaa|a  |Go to address|
IORLW   | 11 1000kkkkkkkk|k  |Inclusive OR literal with W|Z
MOVLW   | 11 0000kkkkkkkk|k  |Move literal to W|
RETFIE  | 00 000000001001| - |Return from interrupt|
RETLW   | 11 0100kkkkkkkk|k  |Return with literal in W|
RETURN  | 00 000000001000| - |Return from Subroutine|
SLEEP   | 00 000001100011| - |Go into standby mode|TP
SUBLW   | 11 1100kkkkkkkk|k  |Subtract W from literal|CDZ
XORLW   | 11 1010kkkkkkkk|k  |Exclusive OR literal with W|Z


  - **decode_hex.py**  : decode heaxdecimal instruction into human readable ascii instruction 
  - **cmp_results.py** : compares results from out and expected output