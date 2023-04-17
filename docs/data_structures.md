## More Data Structures
-----
### <a name="_pdnb0wlyknm2"></a>5.1 Lists  
Dino has support for complex data structures like lists. In dino, users can make lists with elements of all data types and expressions. Dino supports various methods for manipulating lists. The lists are stored in a data type: **ListLiteral**. Lists are indexed starting with 0 to one less than the length of the list.	

Creating a list while assigning it to a variable:

\>>     *assign a = [1, 2+3, 3, 4<5, "i am a string"];*

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

- **list Updation-**

Update a element in the list at index ‘x’ to ‘y’. It is equivalent to **list[x] = y**. x must be in the range from 0 to length of *list* -1.

Example on the previously assigned list ‘a’:

>>a[2] = 4;

>>a;

Output:

ListLiteral(elements=[1, 5, 4, True, StrLiteral(value='i am a string', line=1)], length=5, line=1)

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

- **list.in_list(x)-**

Returns True if x is present in the list, else returns False.

Example:

>>a.in_list(3);

Output:

True

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

*>>	assign dict = {0 : "a", "hello" : 5.2, 1: 3.6};*

Here we have created a dictionary named ‘dict’ which has stored the following key-value pairs:

0 -  “a”

“hello” -  5.2

1 -  3.6

We are yet to add several methods that will help using these dictionaries further. These methods are going to be added very soon.

Methods on dictionaries:

- **dict.add(key, value)-**

Add a key-value pair to the dictionary. If the key already exists, it will update the value of the key.

Example:

*>>	dict.add(3, 30);*

*>>	dict;*

Output:

*DictLiteral(elements={0: StrLiteral(value='a', line=1), 'hello': 5.2, 1: 3.6, 3: 30}, length=4, line=1)*

- **dict Updation-**

Update a value of a key in the dictionary. It is equivalent to **dict[key] = value**.

Example:

*>>	dict[3] = 300;*

*>>	dict;*

Output:

*DictLiteral(elements={0: StrLiteral(value='a', line=1), 'hello': 5.2, 1: 3.6, 3: 300}, length=4, line=1)*

- **dict.at(key)-**

Returns the value of the key in the dictionary. It is equivalent to **dict[key]**.

Example:

*>>	dict.at[3];*

Output:

300

- **dict.keys-**

Returns a list of all the keys in the dictionary.

Example:

*>>	dict.keys;*

Output:

*ListLiteral(elements=[0, 'hello', 1, 3], length=4, line=1)*

- **dict.in_dict(x)-**

Returns True if x is a key in the dictionary, else returns False.

Example:

*>>	dict.in_dict(3);*

Output:

True