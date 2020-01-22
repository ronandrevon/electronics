# PIC16F84A

1. [Features](#features)
1. [Getting started](#getting-started)
2. [Memory and special registers](#memory-and-special-registers)
1. [Instruction set](#instruction-set)
1. [Examples](#examples)
1. [Folders and files](#folders-and-files-structure)
1. [Architecture details](#architecture-details)
1. [Test Status](#test-status)
    - [memory](#memory)
    - [indirect addressing](#fsr)
    - [eeprom](#eeprom)
    - [timer](#tmr0)
    - [function calls](#call)
    - [io](#io)
    - [interrupts](#memory)
    - [mult](#mult)
    - [sleep mode](#sleep)

This architecture is inspired by the 
[PIC16F84A microcontroller](file:///home/ronan/Documents/github/electronics/logisim/PIC16F84A/doc/PIC16F84A.pdf)
designed by microchip.

## Features

General features : 

- 35 instruction set
- 1024 instructions of program memory each 14 bit wide
- 68 General purpose registers each 1 byte wide
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
    - TMR0,  PORTA, PORTB, EEADR,  EEDATA
    - OPTION, TRISA, TRISB, EECON1, EECON2
- PCL/PCLATH jump addressing (for virtual functions)
- 68 bytes of **EEPROM** memory (variable read/write access time)
- SLEEP mode and watchdog timer(**WDT**) to resume



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
- **Load image the binary file programs/bin/test.out into the **FLASH program memory of the PIC19F84A simulator.**
- **MCLR** button used to start (or restarted) the execution.
- **input/output** are the 8 RB7:RB0 and 5 RA4:RA0 pins. By default they are inputs which can be changed during execution with *BSF TRISA (TRISB) \[bit\]* for PORTA (PORTB) 
- Use **Ctrl+E** to enable the clock to tick.
- Use **Ctrl+K** to start ticking (change tick frequency in Simulate -> Tick Frequency).
- Use **Ctrl+T** to tick one at a time
- Monitor the state of each aspects of the CPU through the various probes.

![RAM](file:///home/ronan/Documents/github/electronics/logisim/PIC16F84A/doc/PIC16F84A.png)


## Memory and special registers

The memory is composed of : 
- 68 general purpose registers (**GPR**)
- 68 bytes of **EEPROM** memory
- 2 banks of 12 Special Function Registers (**SFR**) although only 15 physical special function registers exist. The SFR are as follows : 

Name    | bits                                   |hex addr | bank | Description                 
-       |-                                       |-   |-    |-                                  
INDF*   | -                                      | 00 | 0,1 | Used for indirect addressing
TMR0    | TMR0:7-0                               | 01 | 0   | Timer value
OPTION  | RBPU,INTEDG,T0CS,T0SE,PSA,PS:2-0       | 01 | 1   | Option configuration register 
PCL     | PC:7-0                                 | 02 | 0,1 | Low order bits of the program counter
STATUS  | xxRP0,TO,PD,Z,DC,C                     | 03 | 0,1 | Status word register
FSR     | xFSR:6-0                               | 04 | 0,1 | File Select register (pointer)
PORTA   | xxPORTA:4-0                            | 05 | 0   | I/O Port A
TRISA   | xxxTRISA:4-0                           | 05 | 1   | I/O Port A Data direction
PORTB   | PORTB:7-0                              | 06 | 0   | I/O Port B
TRISB   | TRISB:7-0                              | 06 | 1   | I/O Port B Data direction
EEDATA  | EEDATA:7-0                             | 08 | 0   | EEPROM Data register
EECON1  | xxxEEIF,WRERR,WREN,WR,RD               | 08 | 1   | EEPROM configuration register
EEADDR  | EEADDR:7-0                             | 09 | 0   | EEPROM address register
EECON2* | -                                      | 09 | 1   | EEPROM write sequence register
PCLATH  | xxxPC:12-8                             | 0a | 0,1 | high order bits of the program counter
INTCON  | GIE,EEIE,T0IE,INTE,RBIE,T0IF,INTF,RBIF | 0b | 0,1 | Interrupt configuration register

\* Not physical registers

Those bits have the following meaning : 

register    | bit    | Read,Write,reset | Description                
-           |-       |-      |-                                      
**STATUS**  | RP0                     | R/W-0   | Bank select bit
            | TO/PD                   | R  -1   | Time out(0 when WDT occur), power down (0 if SLEEP)
            | Z,DC,C                  | R/W-x   | Zero, Digit carry/borrow, carry/borrow
**OPTION**  | RBPU,INTEDG             | R/W-1   | Port pull up enable, interrupt edge select(1=rising edge)
            | T0CS,T0SE,PSA           | R/W-1   | TMR0 Clock Source Select(1=RA4), TMR0 Source Edge Select Prescaler assignement(1=WDT)
            | PS:2-0                  | R/W-1   | Prescaler rate rate=2^PS
**INTCON**  | GIE,EEIE,T0IE,INTE,RBIE | R/W-0   | Global, EEPROM,TIMR0,RB0,RB7-4 interrupt enable bits
            | T0IF,INTF,RBIF          | R/W-0   | Timer overflow, external, Port change interupt flags(must be cleared in software)
**EECON1**  | EEIF,WRERR,WREN         | R/W-0x0 | EEPROM end write complete interrupt, write error, Write enable
            | WR,RD                   | R/S-0   | EEPROM write, read command (automatically cleared in hardware)


## Instruction set

Each instruction is of the form : 

    label:INSTRUCTION [operand] #Some comment
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
DECFSZ  | 00 1011dfffffff|f,d|Decrement f, Skip if 0|
INCF    | 00 1010dfffffff|f,d|Increment f|Z
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


## Examples
### Multiplcation
- [x] Multiplication program : 
    - [mult_test.pic](file:///home/ronan/Documents/github/electronics/logisim/PIC16F84A/programs/links/mult_test.txt)
    - ADDWF, BSF, DECFSZ, ,BTFSC, GOTO
    - STATUS registers Z and C bits read during execution


## Architecture details

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

## Test status

- [x] compiler *compiler.py* working 
- [x] No errors during NOP

### Memory
- [x] **Memory** access instructions test : 
    - [mem_test.pic](file:///home/ronan/Documents/github/electronics/logisim/PIC16F84A/programs/links/mem_test.txt)
    - MOVWF, MOVF, MOVLW,  CLRF,CLRW 
    - STATUS register written async
    - General purpose registers involved only

### FSR
- [ ] **FSR** File select register indirect addressing feature, **ALU**, **skip**, **GOTO** operations : 
    - [fsr_test.pic](file:///home/ronan/Documents/github/electronics/logisim/PIC16F84A/programs/links/fsr_test.txt)
    - INCF alu operations
    - BTFSS skip based operations
    - GOTO branch operation
    - read, write to FSR
    - indirect addressing read&write
    - STATUS register Z

### Call
- [x] **Call**, **Return** stack involving instructions : 
    - [func_test.pic](file:///home/ronan/Documents/github/electronics/logisim/PIC16F84A/programs/links/func_test.txt)
    - CALL, RETURN, RETLW

### EEPROM
- [x] **EEPROM** read/write access, **bank selection** :
    - [eeprom_test.pic](file:///home/ronan/Documents/github/electronics/logisim/PIC16F84A/programs/links/eeprom_test.txt)
    - read&write to EEPROM
    - BCF
    - write to STATUS:RP0 , write to EEADR, read&write sync&async to EEDAT, read&written sync&async to EECON1

### TMR0
- [ ] **TMR0** Timer clock select, prescaler
    - [tmr0_test.pic](file:///home/ronan/Documents/github/electronics/logisim/PIC16F84A/programs/links/tmr0_test.txt)
    - External clock select T0CS and edge select via T0SE
    - prescaler assignement via PSA and prescaler rate change via PS2:PS0
    - CLRWDT
    - read&write to TMR0 register, write to OPTION register

### IO
- [ ] **I/O** port, state change : 
    - [io_test.pic](file:///home/ronan/Documents/github/electronics/logisim/PIC16F84A/programs/links/io_test.txt)
    - read values on PORTA,PORTB
    - write values on portA, PORTB
    - check INTF and RBIF when both input and output state
    - read, write to PORTA,PORTB registers, write to TRISA,TRISB registers

### INT
- [ ] **Interrupts** and return from interrupts : 
    - [int_test.pic](file:///home/ronan/Documents/github/electronics/logisim/PIC16F84A/programs/links/int_test.txt)
    - external asynchronous on port **RB0/INT**
    - change on ports **RB4:RB7**
    - timer **TMR0** time out
    - data **EEPROM** write complete
    - RETFIE,SWAPF
    - read,write sync&async to intcon register

### SLEEP
- [ ] **Sleep** mode :
    - SLEEP
    - Reset on time out 
    - Reset on interrupt with/without gie
