## More Data Structures
-----
### <a name="_pdnb0wlyknm2"></a>5.1 Lists  
Dino has support for complex data structures like lists. In dino, users can make lists with elements of all data types and expressions. Dino supports various methods for manipulating lists. The lists are stored in a data type: **ListLiteral**. Lists are indexed starting with 0 to one less than the length of the list.	

Creating a list while assigning it to a variable:

\>>     *assign a = [1, 2+3, 3, 4<5, “i am a string”];*

*.>>   a;*

Output:

*ListLiteral(elements=[1, 5, 3, True, StrLiteral(value='i am a string', line=1)], length=5, line=1)*

**Methods on lists:**

- **list.add(x)-**

Add x as an element to the end of the *list*. 

Example on the previously assigned list ‘a’:

>> a.add(“hii”);

>>a;

Output:

ListLiteral(elements=[1, 5, 3, True, StrLiteral(value='i am a string', line=1), StrLiteral(value='hii', line=1)], length=6, line=1)

- **list.at(x)-**

Returns the element at the index ‘x’ in the *list*. It is equivalent to **list[x]**. x must be in the range from 0 to length of *list* -1. 

Example:

>>a.at[2];

Output:

3

- **list.head-**

Returns the first element of the list. Reports error if the list has no elements.

Example:

>>a.head;

Output:

1

- **list.tail-**

Returns a list same as *list* without its first element.

Example:

>>a.tail;



Output:

ListLiteral(elements=[5, 3, True, StrLiteral(value='i am a string', line=1), StrLiteral(value='hii', line=1)], length=5, line=1)

- **list.length-**

Returns the length of the list as an integer.

Example:

>>a.length;

Output:

6

- **list.slice(x, y)-**

Returns a list containing elements starting from the index x till index y-1 in *list*. 

Example:

>>a.slice(2, 4);

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
