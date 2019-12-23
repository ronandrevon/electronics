# electronics
Electronic related projects

## Logisim
Digital simuator of a digital circuits such as chips, processors, microcontrollers,etc ...  

### Appolo 181 4-bit processor

- **appolo.circ** : The digital circuit
- **PROM**        : instruction set image as flashed in PROM
- *dat*
  - *programs* :
    - **ADD**  : performs the basic addition of 2 integers
    - **MULT** : mutliplication of 2 integers
  - *out* : result file of execution of program as run by appolo 
    - result_ADD : result processed by running program ADD  
- *src*
  - **compiler.py**    : compiles a program written in python
  - **decode_hex.py**  : decode heaxdecimal instruction into human readable ascii instruction 
  - **cmp_results.py** : compares results from out and expected output