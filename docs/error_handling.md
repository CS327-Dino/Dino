## Errors and Exceptions
-----

We have mainly 2 types of errors in Dino - Syntax error and Runtime error.

If we use the wrong syntax to write our dino code then our interpreter will throw an error that lets you know that there has been a syntax error. It will also mention the line of error as well as the missing syntax.

As an example if we code the following:

*>>0	assign s = 0;*

   *1	assign a = 3*

   *2	assign b = 6;*

This code will return the following error:

“Error on line 1 : Syntax Error: ’;’ expected after declaration”

We will face similar errors if we code the wrong syntax.

Similarly we have Runtime error which occurs when we code something that goes against the rules of logic of our language.

For example, if we try to call a variable that does not already exist:

*>>0	assign a = 5;*

   *1	assign b = x;*

   *2	assign c = 10;*



Here we will encounter a “Runtime Error on Line 1” as we have used a variable ‘x’ which has not been declared or assigned above.

So, if we try to write dino code that has incomplete or ambiguous syntax, or if the code is not logical as per the rules that we have defined, then our interpreter will throw an Error along with specifying where that error occurred.

Also, if we have errors in multiple lines, dino returns all errors.

*>>0	assign s = 0;*

   *1	assign a = 3*

   *2	assign b = 6;*

   *3	assign c = 5*


This returns the error: “Error on line 2 : Syntax Error:';' expected after declaration

Error on line 4 : Syntax Error:';' expected after declaration”
