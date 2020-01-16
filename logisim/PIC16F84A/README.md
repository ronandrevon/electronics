# PIC16F84A

1. [Getting started](#getting-started)
1. [Instruction set](#instruction-set)
1. [Folders and files structure](#folders-and-files-structure)


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



## 
  - **decode_hex.py**  : decode heaxdecimal instruction into human readable ascii instruction 
  - **cmp_results.py** : compares results from out and expected output