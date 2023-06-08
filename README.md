# Own Programming Language

## A simple compiler which compiles code written in my own programming language into MIPS-Assembler

This is a small project of mine without a real motivation except the learning experience during development itself.
The project is currently in development and only partially functional. However, I will write a small tutorial on how to use my program.

### How it works:

The compiler written in python reads from the file ´bsp.txt´, compiles the code and writes it in the file ´mips1.asm´. This file can then be opened with a MIPS-Simulator like Mars. 
You can try it out by following these steps:

* Open ´bsp.txt´ and write your code using the syntax explained in the next paragraph (then save the file).
* Run ´main.py´. An AST should get printed, which resembles your program.
* Now open ´mips1.asm´ using a MIPS-Simulator of your choice.

If there is no code in the .asm file, check if the function ´from_to_file()´ is called in ´main.py´ and correct if necessary.

### Syntax

This is just some random syntax I like. It might not be the most logical or practical there is.

#### Basics

* No ; are needed
* C-style Braces {} for blocks
* \# for comment and #[...]# for block comment

#### Arithmetic and Logic

The only type is int. Strings and floats are not yet implemented. Booleans are treated like ints, but you can use ´True´ or ´False´ as synonyms for 0 and 1.

* Binary operators: +, -, *, /, &&, ||, mod
* Unary operators: -, !
* Comparators: ==, !=, <, >, <=, >=

#### Variable Declaration, Initialisation and Assignment

Variables have a scope. However, every variable outside a function is global.

* Declaration: ´let x´
* Decl and Init: ´let x = 1´, ´const x = 1´
* Assignment: ´x = 1´

#### Control Flow

* if x < 10 {...}
* while x < 10 {...}
* do, then while x < 10 {...}
* no break yet
* no for-loop yet

#### Functions

Functions can take an infinite number of arguments and return one value. Functions cannot pass other functions.

* Declaration:
    * func aaa: () -> {
    ...
    return 1
    }
    * func bbb: x -> {...}
    * func ccc: (x, y, z) -> {...}
* Call: ´aaa()´, ´ccc(x, y, z)´

#### Lists

* Decl and Init: ´let a = []´, ´let a = [1, 2, 3]´
* Getting an element: ´b = a[4]´
* Reassigning an element: ´a[4] = y´
* Binary operators:
    * Use ´push´ to append a list: ´a push 4´ (returns the appended list)
    * pop coming soon
    * Use ´add´ to append a list by a second list: ´a add b´ (returns the appended list)
* Unary operators: 
    * ´len´ yields the length of the list: ´let lenOfA = len a´
    * ´copy´ returns a pointer to a copy of the list: ´let copyOfA = copy a´
    * ´pop´ returns the last element of the list and removes it from the list: ´let x = pop a´
* Comparators: 
    * ´in´ checks if left argument is in right one: ´if x in [1, 2, 3] {...}´
    * ´equals´ checks if both lists have the same elements: ´if a equals b {...}´

If you find any bugs or want to share your opinion about this project, feel free to open a discussion or issue. 
And sorry if my code is full of mixed German and English.






