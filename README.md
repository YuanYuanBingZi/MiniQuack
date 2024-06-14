# Nano Quack & Mini Quack & Whole Quack- The project of CS 461 at UO
The basic framework of this project is forked by the sample code from "Lark Grammar to AST and Symbol Table". Here is its original description: A small example of parsing some parts of the Quack language (class and method declarations), transforming the Lark parse tree into an AST with our own custom classes, and then walking the AST to populate a symbol table with class and method declarations. Thanks to Pranav Mathur for the initial symbol table of built-in classes (in `qklib/builtin_methods.json`).I have followed that structure in filling in additional classes and methods from the source file. 


# Nano Quack
This is the second project of CS 461. Its requirement includes:  
1. Parse some basic sentences for Quack Language  
2. Not include control flow  
   no if statements, no while statements  
3. Each Assignment includes the Type Declaration   
   Example: `x: Int = 13 + y;`  
4. Hold Static Checking  
   Example: `x: Int = "Why would you " + "do this?" - 3;`  
   we will translate it without complaint.  It will probably cause car crashes, house fires, and seg   faults, but nano-quack has no protections against any of that. (from Professor Michal)  

# Mini Quack
Mini-Quack is the third project of CS 461. It includes control flow and type inference.

## Project Structure

- `qklib/`: Contains the necessary parsing files for Quack.
  - `quack_grammar.txt`: Grammar Definition.
  - `quack_ast.py`: Build AST Nodes.
  - `quack_parser.py`: Parser implementation.
  - `quack_transformer.py`: AST transformation logic.
  - `quack_type_inference.py`: Type inference logic.
      
- `samples/`: Contains sample test cases.
   - `BasicFunction/`: Test Cases for basic function testing.
      - `test1_Int.qk`: Int Assignment with Add, Sub Op
      - `test2_Float.qk'`: Float Assignment with Mul, Div Op
      - `test3_String.qk'`: String Assignment with Add Op
      - `test4_Call.qk'`: Method Call with Int, Float, String Type
      - `test5_If.qk'`: Control Flow: If Statement
      - `test6_While.qk'`: Control Flow: While Statement
   - `TypeInference/`: Test Cases for Type Inference testing.
      - `test1_TypeOperations.qk`: Same Type Add/Sub/Mul/Div for Int, Float, String
      - `test2_TypeMismatch.qk'`: Error of TypeMismatch
      - `test3_VarNotdefined.qk'`: Error of VarNotDefined
      - `test4_Boolean.qk'`: Boolean Assignment, Boolean Type for logic Op
      - `test5_functions.qk'`: Function Declaration
   - `blahblahblah.qk`: original test code
   - `formals.qk`: original test code
   - `ifelse`: original test code
  
- `OBJ/`: Contains generated assembly or object files.
- `quack.sh`: Script to compile and run a Quack program.
- `quackc.sh`: Script to compile a Quack program without running it.

# Whole Quack
I add the code generation file to generate assembly code.
Now it can be tested with a simple quack program about Integer Assignment.

The Quack code is:
```python
a: Int = 15;
b: Int = 9;
c: Int = a + b;
d: Int = c - 5;
```

The Assembly Tree generate by the Grammar is:
```python
AST Tree: Block([Assign(a, Int, Int(15)), Assign(b, Int, Int(9)), Assign(c, Int, Add(Var(a), Var(b))), Assign(d, Int, Sub(Var(c), Int(5)))])
```

The target code generation is:
```python
Code Generation: 
alloc 4
const 15
store 0
const 9
store 1
load 0
load 1
call Int: plus
store 2
load 2
const 5
call Int: minus
store 3
```


## To Run

You must install lark before running. 
You can install it in a virtual 
environment as follows:
```shell
python3 -m venv env
. env/bin/activate
pip3 install -r requirements.txt
```

The second command above (with `activate`)
makes the virtual environment active. 

To run: 
```shell
python3 quack_front.py samples/blahblahblah.qk
```
The output should be a poorly indented
version of blahblahblah.qk with some 
"normalization", e.g., the constructor
methods are included as if they had been
enclosed in a method declaration.  Following
that you should find a symbol table
consisting of the contents of 
`builtin_methods.json` and a similar
record for the method `Point` from 
blahblahblah.  

To leave the virtual environment after
running the sample, you can use this 
command: 

```shell
deactivate
```
