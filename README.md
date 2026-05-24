# What is VMEMU?

VMEMU (Virtual Machine Emulator) is a custom Python-based CPU simulator that emulates a custom CPU variant (which i made) called NanoCore-x5/ncx5. It also has its own lightweight set of Assembly.

# Disclaimer

This is still a bit unstable. It is only 1 day old and was meant to be a small side-project before my exams. Some parts are AI-generated, but not the crucial parts. I mostly wrote the code myself.

# Emulator specs

This emulator comes with:

- 5 registers from x0 to x4
- 16 bytes of R/W RAM
- A simple and lightweight set of Assembly.

# The basics of ncx5 Assembly (and all its commands)


- mov  

  Usage: Copy a value into a register  

  Example: mov x0, 5

- add  

  Usage: Add two values and store the result  

  Example: add x2, x0, x1

- sub  

  Usage: Subtract two values and store the result
  
  Example: sub x3, x0, 2

- mul

  Usage: Multiply two values and store the result
  
  Example: mul x4, x1, 3

- cmp

  Usage: Compare two values and set flags
  
  Example: cmp x0, x1

- b

  Usage: Jump to an address or label unconditionally
  
  Example: b _loop

- b.eq  

  Usage: Jump if the last compare was equal
  
  Example: b.eq _yay

-b.ne

  Usage: Jump if the last compare was not equal  

  Example: b.ne _skip

- nop  

  Usage: Do nothing for one cycle  

  Example: nop

- ret  

  Usage: Stop execution and halt system

  Example: ret

- edr  

  Usage: Write a register value to RAM in binary

  Example: edr 0x0, 00000000 000000101

- rde  

  Usage: Read a value from RAM into a register
  
  Example: rde x1, 0x10

- Assembly labels  

  Usage: Mark a spot in code for jumping. Basically like def in Python

  Example: _loop:

- run

  Usage: Execute all buffered instructions (and quit at the same time)  

  Example: run

- al.r

  Usage: Re-resolve labels and execute everything  

  Example: al.r

# Creating and running pre-boot programs

- Creating programs

First off, you will have to make a new .py program.

Then, you will make a variable (e.g code) and make it as `"""` instead of `"`. This is where you place the code.

After that, print the code by running `print(code)`. 

For an example, please check the EXAMPLE.py in this repository.

- Running programs

To run programs in VMEMU, use the `-l` or `--load` argument before running the main file. Such as:

`./vmemu.py -l ./EXAMPLE.py`

# What can VMEMU be used for?

VMEMU can be used for many reasons. Such as:

- Tinkering, quickly experimenting and messing around

- Educational purposes.





