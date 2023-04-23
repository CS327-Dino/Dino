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

## Quick Startup

- Clone the repository using the following command:<br>
	`git clone https://github.com/CS327-Dino/Dino.git`
- Navigate to the Dino directory.
- Run the following command to start the Dino prompt:<br>
	`python main.py`
- To run a code file, use the following command:<br>
	`python main.py {file_name}`
- To run the Dino prompt with verbose, use the following command:<br>
	`python main.py -v`
- To run a code file with verbose, use the following command:<br>
	`python main.py {file_name} -v`
- To get the time of execution of a code file, use the following command:<br>
   `python main.py {file_name} -t`
- To exit the compilation process at any point, either close the Dino prompt or exit from a code file, use the abort utility provided,<br>
	`abort();`

-----
## Tests
* To run specific tests, use the following command:<br>
	make check FILE={file_name}
* To run all tests, use the following command:<br>
	make checkall
-----
### Euler 14
To run euler 14 test file, use the following command:
```bash
python main.py euler14.dino
```
Results of Euler14 are here: [euler14_Results.md](./docs/euler14_Results.md)

-----
## The Dino Tutorial


1. [Using the Dino Interpreter](./docs/usage.md)………………………………………………………………….
1. [Variables in Dino](./docs/variables.md)……………………………………………………………………………
   1. Defining Variables
   1. Scoping
1. [Numbers and Strings: Datatypes](./docs/data_types.md).……………………………………………………..
1. [Control Flow Tool](./docs/control_flow.md)
   1. if Statement…………………………………………………………………………
   1. loop Statement……………………………………………………………………...
   1. for loop Statement…………………………………………………………………
   1. Defining Functions………………………………………………………………….
   1. Calling Functions…………………………………………………………………...
   1. Lambda Expression…………………………………………………………………
1. [More Data Structures](./docs/data_structures.md)
   1. Lists…………………………………………………………………………………
   1. Dictionary…………………………………………………………………………..
1. [Input and Output](./docs/IO.md)
   1. capture Keyword…………………………………………………………………....
   1. echo Keyword……………………………………………………………………....
1. [Comments](./docs/comments.md)…………………………………………………………………………………..
1. [Errors and Exceptions](./docs/error_handling.md)………………………………………………………………………
----
Here is a list of all the goals our project has met under the CS-327 course goals list:

M - Minimal Goals
I - Intermediate Goals
A - Advanced Goals

- M: A number type and arithmetic.
- I: Multiple number types such as fractions and integers. Quotient and division are different. Quotient has type (integer, integer) -> integer and division has type (fraction, fraction) -> fraction. An integer can be used wherever a fraction can be used.
- M: Mutable variables.
- M: Let expressions.
- M: A Boolean type, comparisons, and if-else.
- I: An explicit unary boolifying operator. In Perl so x where x has any type produces a Boolean value. For example, if x is a number, it is true when non-zero. If x is a string, it is true when non-empty.
- I: Static type checking. The expression (5>3) + 2 should be an error without evaluating anything.
- M: Strings with concatenation and slicing.
- M: A print operation that prints values to screen.
- M: loops.
- M: Functions
- M: Lists with operations cons, is-empty?, head, tail.
- I: for loop to iterate over lists.
- I: Mutable arrays with indexing, appending, popping, concatenation, element assignment.

List of Goals that are yet to be implemented:

- I: Parallel let (See let..and in Ocaml).
- A: Disallow mutable variables to change type. With the binding let mut p = True in ..., the variable p should only be assigned boolean values.
- I: Allow declaration of type of array. For example let xs: Array[int] = [] in ... should prevent xs[0] ← 5/3.
- A: Step-by-step debugger for your programming language.
- A: User-defined types – records.
- A: First-class functions.

----
**Github Repo: [CS327-Dino/Dino (github.com)](https://github.com/CS327-Dino/Dino)**
-----