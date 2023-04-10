 # Dino

**Indian Institute of Technology, Gandhinagar**

**Dino Documentation**

-----

**CS 327: Compilers**

Last Update: 19th March 2023


**Authors**


|Name|Roll Number|
| :-: | :-: |
|Harshvardhan Vala|20110075|
|Inderjeet Singh bhullar|20110080|
|Kalash Kankaria|20110088|
|Kanishk Singhal|20110091|
|Lipika Rajpal|20110102|


***Under the guidance of***
Prof. Balagopal Komarath

-----
## Tests
* To run specific tests, use the following command:<br>
	`make check FILE={file_name}`
* To run all tests, use the following command:<br>
	`make checkall`

-----
## The Dino Tutorial


1. [Using the Dino Interpreter](#using-the-dino-interpreter)………………………………………………………………….
1. [Variables in Dino](#variables-in-dino)……………………………………………………………………………
   1. Defining Variables
   1. Scoping
1. [Numbers and Strings: Datatypes](#numbers-and-strings-datatypes).……………………………………………………..
1. [Control Flow Tool](#control-flow)
   1. if Statement…………………………………………………………………………
   1. loop Statement……………………………………………………………………...
   1. Defining Functions………………………………………………………………….
   1. Calling Functions…………………………………………………………………...
   1. Lambda Expression…………………………………………………………………
1. [More Data Structures](#more-data-structures)
   1. Lists…………………………………………………………………………………
   1. Dictionary…………………………………………………………………………..
1. [Input and Output](#input-and-output)
   1. capture Keyword…………………………………………………………………....
   1. echo Keyword……………………………………………………………………....
1. [Comments](#comments)…………………………………………………………………………………..
1. [Errors and Exceptions](#errors-and-exceptions)………………………………………………………………………






----
**Github Repo: [CS327-Dino/Dino (github.com)](https://github.com/CS327-Dino/Dino)**

-----
## Using the Dino Interpreter
-----
**Open the Dino Prompt**

Simply run the main.py file

\>>	python main.py

**Run a Code File**

\> Run the main.py file with the argument as the name of the file you want to run

\> If you want to run the file test.dino:

\>>	python main.py test.dino

**Run the Dino Prompt with Verbose**

\> To also output the parsed and resolved expressions of the code, use the verbose utility by using the extension -v

\>>	python main.py -v

**Run a Code File with Verbose**

\>>	python main.py test.dino -v

**To exit**

\> To exit the compilation process at any point, either close the Dino prompt or exit from a code file, use the abort utility provided,

\>>	abort();

Output: Program Aborted




## Variables in Dino
-----

#### <a name="_udl7hgjt7da7"></a>2.1 Defining Variables
Variables are the containers in which we can store data in the memory and access it later.

` `In **Dino** we give users to define two types of container-

- Using *assign* keyword- Containers defined by this method can be reassigned with different values.
- Using *const* keyword- These containers have constant value and can not be reassigned with different values.

E.g.-

|<p>assign a = 3;</p><p>echo(a+5);</p>|<p>const a = 3;</p><p>echo(a+5);</p>|
| :- | :- |
#### <a name="_1v1zt2dthkog"></a>2.2 Scoping
The scoping of vaiiables in **Dino** is lexical scoping. The language does a resolution pass before evaluation to determine the mapping of which variable refers to which position.This helps us easily evaluate cases like-

*assign a = 5;*

*if(a>5)*

`	`*assign a = 10;*

`	`*echo(a);*

*end*

*else*

`	`*assign a = 15;*

`	`*echo(a);*

*end*

*echo(a); ? Outputs: 15 5*
## Numbers and Strings: Datatypes
-----
The Dino language supports the following datatypes:

Numerical

- Integer (IntLiteral)
- Decimal (NumLiteral)

Non-Numerical

- String (StrLiteral)
- Boolean (BoolLiteral)
- Null (NullLiteral)

**Note:** The language uses dynamic datatype assignment. 

The following binary arithmetic operations can be performed on all the numeric data types. The operators are ordered in descending order of priority. 


|**Operation**|**Result**|
| :- | :- |
|x ^ y|x raised to y|
|x \* y|Product of x and y|
|x / y|x divided by y|
|x + y|Sum of x and y|
|x - y|Difference of x and y|
|x % y|Remainder of x / y|

The following table has the bitwise and logical operations ordered as decreasing priority. The bitwise operations can only be performed on integral values (IntLiteral). Logical operations can be applied on all data types (numerical and non-numerical). 


|**Operation**|**Result**|**Notes**|
| :- | :- | :- |
|x or y|logical ‘*or*’ on x and y|Returns a boolean|
|x and y|logical ‘*and*’ on x and y|Returns a boolean|
|x | y|Bitwise ‘*or*’ of x and y|Operands must be IntLiteral (s)|
|x & y|Bitwise ‘*and*’ of x and y|Operands must be IntLiteral (s)|

**Unary Operations-** 

Dino supports two variations of the negation as a unary operation:

- The bang (!) can be used to negate all the data types and complex expressions. It returns a boolean. 
- The dash (-) can only negate the numeric data types (IntLiteral and NumLiteral). It multiplies their value by -1. For expressions like - *boolean,* False is considered as the integer 0 and True is considered as 1. 


|**Operation**|**Result**|**Notes**|
| :- | :- | :- |
|! x|<p>If x is true, return false. </p><p>Else, return true</p>||
|-x |Multiply x with -1|x must be numeric or boolean|
|++ x|Increment x by 1|x must be numeric or boolean|
|-- x |Decrement x by 1|x must be numeric or boolean|

**Comparison operators -**


|**Operation**|**Result**|
| :- | :- |
|x < y|True if x is strictly less than y|
|x > y|True if x is strictly greater than y|
|x <= y|True if x is less than  or equal to y|
|x >= y|True if x is greater than  or equal to y|
|x == y|True if value of x is equal to y|
|x != y|True if value of x is not equal to y |
** 

The priority of the operators in decreasing order:

Unary Operators (Negation)

Exponential(^)

Multiplication and Division(\*, /)

Addition and Subtraction(+ , -)

*Bitwise AND (&)*

*Bitwise OR (|)* 

*Logical AND (and)*

*Logical OR (or)*

Comparison (<, >, <=, >=)

Equality comparison (==, !=)

Here are some examples of operations on the defined data types executable in Dino-

**Addition**

\>>	3 + 5;

Output: 8

\>>	3 + 2.8;

Output: 5.8

\>>	“Hello ” + “World”;

Output: Hello World

\>>	“Hello ” + 3;

Output: Runtime Error at 1 : Error: '+' operation valid only for two strings or two numerical values


## Control Flow
-----

### <a name="_mdu1cewc16ik"></a>4.1 If Statement
`	`The language handles conditional statements using the if-else statement

`	`Syntax:

`		`*if (<condition>)*

`			`*<if block body>*

`		`*end*

`		`*else*

`			`*<else block body>*

`		`*end* 

`	`If there is no else-block, then the syntax is:



*if (<condition>)*

`			`*<if block body>*

`		`*end*



`	`Examples:

\>>	assign num = 20;

if(num % 2 == 0)

`    `echo("Even");

end

else

`    `echo("Odd");

end

`	`Output: Even

### <a name="_1j1x3aor4k"></a>4.2 Loops
`	`The usual While loop in most languages is used in the following manner in Dino.

`	`Syntax:

`		`*loop (<condition>)*

`			`*<body>*

`		`*end* 



`	`Examples:

\>>	assign num = 20;

loop(num >10)

`    `echo(num);

`    `num = num - 1;

end

`	`Output: 

`		`20

`		`19

`		`18

`		`17

`		`16

`		`15

`		`14

`		`13

`		`12

`		`11
### <a name="_7uzr0bwlygr2"></a>4.3 Defining Functions
Functions in Dino are code blocks having their own scope that can be used multiple times by calling them anywhere else in the code.

We create functions using the “func” keyword followed by the arguments of the code block.

We end the function declaration using the “end” keyword.

Here’s an example of how we create functions in Dino:

*>>       func fact(n)*

`    `*if (n == 0)*

`        `*return 1;*

`    `*end*

`    `*else*

`        `*return n \* fact(n-1);*

`    `*end*

*end*

This is a recursive function to calculate the factorial of an input number ‘n’

The return keyword outputs the expression written in front of it when this function is called.

Here’s declaring a function without the return keyword:

\>>	*func g(a, b, c)*

`	    `*assign s = a+b+c;*

`    `*echo(s);*

*end* 

This function will not return anything but will print out the sum of a, b and c inputs.

### <a name="_4co2pisyegdt"></a>4.4 Calling Functions
We know how we will create/ declare functions in the above section, now we need to call the functions that we have declared. 

We call a function when we need to run the code block inside the function and we can even use the output expression/ the return expression of that function.

In order to call a function, we simply need to type the name of the function along with the parameters that we will pass for that function.

Here we will create a function named ‘sum’: 

\>>	*func sum(a, b, c)*

`	    `*assign s = a+b+c;*

`    `*return s;*

*end* 

Now we will call this function for some 3 numbers:

*>>	assign s = sum(2, 3, 5);*

`	`*echo(s);*

This will print ‘10’ as the function sum will return 2+3+5 = 10. 

Similarly, if we declare:

*>>	func do\_this()*

`	    `*echo(“Hello World”);*

`	`*end*



`	`*do\_this();*

Here we declare and then call the function ‘do\_this’ which will print out “Hello World” to the terminal as that is what this function does.

### <a name="_13bpmiig72f3"></a>4.5 	Lambda Expressions
Lambda expressions work like let expressions. Lambda expressions enable users to define anonymous functions that can be used within other functions or

expressions. It allows users to define and bind values to identifiers. This enables the creation of local variables, which can be used in expressions or other functions defined within the scope of the lambda expression.


Here is how to use lambda expressions: 

\>>*echo(lambda a = 12 in lambda b = 7 in b\*b+a end end);*

The above line prints 61 *(7\*7+12)*

A few other examples: 

\>> *func sum(a, b, c)*

`	    `*assign s = a+b+c;*

`    	    `*return s;*

`    `*end* 

`   `*echo(lambda x = 12 in sum(x,5,6) end);*

This outputs 23

`          `*>> echo(lambda a=2 in a\*(lambda b=1 in lambda a=10 in b+a\*b end end) end;)*

This outputs 22  *(2\*(1+10))*
## More Data Structures
-----
### <a name="_pdnb0wlyknm2"></a>5.1 Lists  
Dino has support for complex data structures like lists. In dino, users can make lists with elements of all data types and expressions. Dino supports various methods for manipulating lists. The lists are stored in a data type: **ListLiteral**. Lists are indexed starting with 0 to one less than the length of the list.	

Creating a list while assigning it to a variable:

\>>     *assign a = [1, 2+3, 3, 4<5, “i am a string”];*

*.>>   a;*

Output:

`	`*ListLiteral(elements=[1, 5, 3, True, StrLiteral(value='i am a string', line=1)], length=5, line=1)*

**Methods on lists:**

- **list.add(x)-**

Add x as an element to the end of the *list*. 

Example on the previously assigned list ‘a’:

`	`>> a.add(“hii”);

`	`>>a;

Output:

ListLiteral(elements=[1, 5, 3, True, StrLiteral(value='i am a string', line=1), StrLiteral(value='hii', line=1)], length=6, line=1)

- **list.at(x)-**

Returns the element at the index ‘x’ in the *list*. It is equivalent to **list[x]**. x must be in the range from 0 to length of *list* -1. 

Example:

`	`>>a.at[2];

Output:

3

- **list.head-**

Returns the first element of the list. Reports error if the list has no elements.

Example:

`	`>>a.head;

Output:

1

- **list.tail-**

Returns a list same as *list* without its first element.

Example:

`	`>>a.tail;



Output:

ListLiteral(elements=[5, 3, True, StrLiteral(value='i am a string', line=1), StrLiteral(value='hii', line=1)], length=5, line=1)

- **list.length-**

Returns the length of the list as an integer.

Example:

`	`>>a.length;

Output:

6

- **list.slice(x, y)-**

Returns a list containing elements starting from the index x till index y-1 in *list*. 

Example:

`	`>>a.slice(2, 4);

Output:

ListLiteral(elements=[3, True], length=2, line=1)

### <a name="_q3xbhn4f26ez"></a>5.2 Dictionary  
Dino also supports a data type similar to hash-maps known as “Dictionary.” In these dictionaries we can store key-value pairs where each key must be unique.

In order to create a dictionary, we can simply use the assign keyword along with curly braces to initialize the dictionary.

Example:

*>>	assign dict = {0 : “a” , 1 : “b”, 2  : “c”};*

Here we have created a dictionary named ‘dict’ which has stored the following key-value pairs:

0 -  “a”

1 -  “b”

2 -  “c”

In dino, we can have both key and values of either Integer, float or string data type. 

So, we can even create such a dictionary:

*>>	assign dict = {0 : “a”, “hello” : 5.2, 1: 3.6};*

Here we have created a dictionary named ‘dict’ which has stored the following key-value pairs:

0 -  “a”

“hello” -  5.2

1 -  3.6

We are yet to add several methods that will help using these dictionaries further. These methods are going to be added very soon.








## Input and Output
-----
### <a name="_1v8ezztxexcy"></a>6.1 Input
`	`The Dino language provides the utility to accept user-input to the programmer and then use that 
`	`input and store it in a variable to be used further in the program.

`	`Syntax:

`		`*capture(<Text to be displayed>)*



- This can be used as an input to a variable
- It can be printed directly to the terminal with or without some manipulation

`	`Examples:

\>>	assign num = capture(“Enter Number ”);

`	`num = num + 5;

`	`Output: 

`		`Enter Number 10

`		`// num stores the value 15

`	`>>	if (capture(“Enter Number ”) != 2)

`			`num = num + 5;

`		`end

`	`Output: 

`		`Enter Number 2

`		`// num stores the value 2



`		`Enter Number 7

`		`// num stores the value 12

### <a name="_iazpu2tlqds6"></a>6.2 Output
`	`The Dino language provides the utility of the usual print statement, i.e., to write the output to 
`	`the console using the echo command.

`	`Syntax:

`		`*echo(<Output to be displayed>);*



- Any Variable/ Literal can be passed to this function
- It can also take an expression as input and output the evaluated expression

`	`Examples:

\>>	echo(“Hello World”)

[A classic example of “I know how to write Hello World in many programming languages”]

Output: 

`		`Hello World

\>>	echo(3+5^2)

`	`Output: 

`		`28


## Comments
-----

Comments are the part of code that is not executed while running. They make it easier for

users to document their code and improve readability.

There may be single line as well as multiline comments. 

Single line comment: 

They start by using ‘?’. 

The entire line after the occurrence of ‘?’ is commented out. 

*>> ?This is a single line comment* 

Multiline comment: 

Multiline comments can be used by using ‘?:’ and ‘:?’. The entire text between these two symbols is commented out. 

For eg: 

*>> echo(2);*

`    `*?: This entire*

`        `*block of* 

`       `*code is*

`       `*not executed.* 

`   `*:?*  

`   `*assign a=3;*







## Errors and Exceptions
-----

We have mainly 2 types of errors in Dino - Syntax error and Runtime error.

If we use the wrong syntax to write our dino code then our interpreter will throw an error that lets you know that there has been a syntax error. It will also mention the line of error as well as the missing syntax.

As an example if we code the following:

*>>0	assign s = 0;*

`     `*1	assign a = 3*

`     `*2	assign b = 6;*

This code will return the following error:

“Error on line 1 : Syntax Error: ’;’ expected after declaration”

We will face similar errors if we code the wrong syntax.

Similarly we have Runtime error which occurs when we code something that goes against the rules of logic of our language.

For example, if we try to call a variable that does not already exist:

*>>0	assign a = 5;*

`     `*1	assign b = x;*

`     `*2	assign c = 10;*



Here we will encounter a “Runtime Error on Line 1” as we have used a variable ‘x’ which has not been declared or assigned above.

So, if we try to write dino code that has incomplete or ambiguous syntax, or if the code is not logical as per the rules that we have defined, then our interpreter will throw an Error along with specifying where that error occurred.

Also, if we have errors in multiple lines, dino returns all errors.

*>>0	assign s = 0;*

`     `*1	assign a = 3*

`     `*2	assign b = 6;*

`     `*3	assign c = 5*


This returns the error: “Error on line 2 : Syntax Error:';' expected after declaration

Error on line 4 : Syntax Error:';' expected after declaration”
