## Control Flow
-----

### <a name="_mdu1cewc16ik"></a>4.1 If Statement
The language handles conditional statements using the if-else statement

Syntax:

		*if (<condition>)*

			*<if block body>*

		*end*

		*else*

			*<else block body>*

		*end* 

If there is no else-block, then the syntax is:



      *if (<condition>)*

			*<if block body>*

		*end*



Examples:

\>>	

      assign num = 20;

      if(num % 2 == 0)

         echo("Even");

      end

      else

         echo("Odd");

      end

Output: Even

### <a name="_1j1x3aor4k"></a>4.2 Loops
The usual While loop in most languages is used in the following manner in Dino.

Syntax:

		*loop (<condition>)*

			*<body>*

		*end* 



Examples:

\>>	
      
      assign num = 20;

      loop(num >10)

         echo(num);

         num = num - 1;

      end

Output: 

		20

		19

		18

		17

		16

		15

		14

		13

		12

		11

### <a name="_1j1x3aor4k"></a>4.3 For Loops
For loops are just sugared while loops that make iterations easier.
The usual For loop in most languages is used in the following manner in Dino.

Syntax:

		*iterate (<iterator>;<condition>;<increment>)*

			*<body>*

		*end* 



Examples:

\>>	
      
      assign i = 1;

      iterate(i=2; i<100; i*2)

         echo(i);

      end

Output: 

		2

		4

		8

		16

		32

		64

\>>	
      
      iterate(assign i=1; i<100; i*2)

         echo(i);

      end

Output: 

		1

		2

		4

		8

		16

		32

		64



### <a name="_7uzr0bwlygr2"></a>4.3 Defining Functions
Functions in Dino are code blocks having their own scope that can be used multiple times by calling them anywhere else in the code.

We create functions using the “func” keyword followed by the arguments of the code block.

We end the function declaration using the “end” keyword.

Here’s an example of how we create functions in Dino:

*>>       func fact(n)*

*if (n == 0)*

   *return 1;*

*end*

*else*

   *return n \* fact(n-1);*

*end*

*end*

This is a recursive function to calculate the factorial of an input number ‘n’

The return keyword outputs the expression written in front of it when this function is called.

Here’s declaring a function without the return keyword:

\>>	*func g(a, b, c)*

   *assign s = a+b+c;*

*echo(s);*

*end* 

This function will not return anything but will print out the sum of a, b and c inputs.

### <a name="_4co2pisyegdt"></a>4.4 Calling Functions
We know how we will create/ declare functions in the above section, now we need to call the functions that we have declared. 

We call a function when we need to run the code block inside the function and we can even use the output expression/ the return expression of that function.

In order to call a function, we simply need to type the name of the function along with the parameters that we will pass for that function.

Here we will create a function named ‘sum’: 

\>>	*func sum(a, b, c)*

   *assign s = a+b+c;*

*return s;*

*end* 

Now we will call this function for some 3 numbers:

*>>	assign s = sum(2, 3, 5);*

*echo(s);*

This will print ‘10’ as the function sum will return 2+3+5 = 10. 

Similarly, if we declare:

*>>	func do\_this()*

*echo(“Hello World”);*

*end*



*do\_this();*

Here we declare and then call the function ‘do\_this’ which will print out “Hello World” to the terminal as that is what this function does.

### <a name="_13bpmiig72f3"></a>4.5 	Lambda Expressions
Lambda expressions work like let expressions. Lambda expressions enable users to define anonymous functions that can be used within other functions or

expressions. It allows users to define and bind values to identifiers. This enables the creation of local variables, which can be used in expressions or other functions defined within the scope of the lambda expression.


Here is how to use lambda expressions: 

\>>*echo(lambda a = 12 in lambda b = 7 in b\*b+a end end);*

The above line prints 61 *(7\*7+12)*

A few other examples: 

\>> *func sum(a, b, c)*

*assign s = a+b+c;*

   *return s;*

*end* 

   *echo(lambda x = 12 in sum(x,5,6) end);*

This outputs 23

*>> echo(lambda a=2 in a\*(lambda b=1 in lambda a=10 in b+a\*b end end) end;)*

This outputs 22  *(2\*(1+10))*