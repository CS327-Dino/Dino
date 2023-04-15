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