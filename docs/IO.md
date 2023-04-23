## Input and Output
-----
### <a name="_1v8ezztxexcy"></a>6.1 Input
The Dino language provides the utility to accept user-input to the programmer and then use that 
input and store it in a variable to be used further in the program.

Syntax:

*capture(<Text to be displayed>)*



- This can be used as an input to a variable
- It can be printed directly to the terminal with or without some manipulation

Examples:

\>>	

assign num = capture(“Enter Number: ”);

num = num + 5;

Output: 

		Enter Number:
	  // num stores the number entered by the user
      // num = num + 5

\>>	

assign num = capture();

num = num + 5;

Output: 

	  // num stores the number entered by the user
      // num = num + 5  


### <a name="_iazpu2tlqds6"></a>6.2 Output
The Dino language provides the utility of the usual print statement, i.e., to write the output to 
the console using the echo command.

Syntax:

		*echo(<Output to be displayed>);*



- Any Variable/ Literal can be passed to this function
- It can also take an expression as input and output the evaluated expression

Examples:

\>>	echo(“Hello World”)

[A classic example of “I know how to write Hello World in many programming languages”]

Output: 

		Hello World

\>>	echo(3+5^2)

Output: 

		28
