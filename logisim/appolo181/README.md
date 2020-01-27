# Apollo181

1. [features](#features)
1. [Getting started](#getting-started)
1. [Instruction set](#instruction-set)
1. [Folders and files structure](#folders-and-files-structure)

## Features

The apollo181 is a home made processor created by [Gianluca G.](https://apollo181.wixsite.com/apollo181). 
Here is an inspired Logisim simulator version of it. 
General features : 

- 11 instruction set
- 4x4 bit registers 
- 256 instructions of program memory each 8 bit wide
- 4 input ports and 4 output ports
- conditional and unconditional program branching instructions

## Getting started

The simulator can be lauchned with : 

    logisim appolo181.circ &
A program can be written in an assembler ***file*.apl** file (see 
[Instruction set](#instruction-set) to learn this basic language and 
[add.apl](#), [mult.apl](#) to see some examples).
The programs can be compiled using the compiler *compiler.py* written in
python3. For example the mult program would be compiled with : 

    ./compiler.py programs/mult.apl -e -v
where 
- -e : option to display encoded information (highly recommended)
- -v : verbose option

A binary file **bin/mult.out** has been produced. Then :
- load the binary file **programs/bin/mult.out** into the **program RAM memory** of the Apollo simulator.
- The execution can be started using **START** button.
- The 4 **inputs** can be modified at will.
- The **RESET** button can be used at anytime to reset the CPU to original state.
- Use **Ctrl+E** to enable the clock to tick.
- Use **Ctrl+K** to start ticking.
- Use **Ctrl+T** to tick one at a time
- Monitor the state of each aspects of the CPU through the probes of the *Monitoring* panel. In particular, the output of the computation can be seen in the *MEMORY/Outputs* tab.

![RAM](file:///home/ronan/Documents/github/electronics/logisim/appolo181/doc/apollo181.png)




## Instruction set 

Each instruction is of the form : 

    label : INSTRUCTION DAT #Some comment
where : 
- **label** is optionally used to refer to a specific location for jump instructions
- **INSRUCTION** must belong to the instruction set below
- **DAT** is a 4-bit number between 0-15
- **\#** Anything after this character is a comment and therefore not compiled

| Instruction | Description  |
--------------|--------------|
| NOPE        | no operation |
| JUMP        | jump to location labeled by DAT |
| JUMPZ       | jump to location labeled by DAT if status flag Z=1 |
| LOADRW      | load register R=DAT with accumulator W |
| LOADWR      | load accumulator W with register R=DAT |
| CMPWR       | Sets status flag Z=1 if accumulator W equals register R=DAT |
| ADDWR       | Adds accumulator W with register R=DAT. Sets status flag C=1 if carry arises |
| LOADWL      | load accumulator W with litteral DAT |
| CMPWL       | Sets status flag Z=1 if accumulator W equals litteral DAT |
| ADDWL       | Adds accumulator W with litteral DAT. Sets status flag C=1 if carry arises |
| IN          | Load accumulator W with input IN=DAT |
| OUT         | Write to output OUT=DAT with accumulator W |

## Folders and files structure

- **appolo181.circ** : The digital circuit simulating the Appolo181 architecture
- **compiler.py**    : Compiles a program written in *file*.apl
- **PROM.py**        : Used to generate the PROM image and PROM.pkl file
- *dat*
    - **PROM**     : Instruction set image as flashed in PROM
    - **PROM.pkl** : Dataframe containing useful information about the data in PROM
- *programs* :
    - **add.apl**   : Addition of 2 integers
    - **mult.apl**  : Mutliplication of 2 integers
    - **bin/**          : Compiled binary(hex encoding) files to flash into Appolo memory 
- *doc* 
    - **apollo181Gianluca.pdf** : The original architecture
    - **CPU.png**               : The logisim version of the Appolo181 CPU
    - **apollo181.png**         : The input output setup to interact with the Appolo181 CPU