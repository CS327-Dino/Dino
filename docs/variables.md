## Variables in Dino
-----

#### <a name="_udl7hgjt7da7"></a>2.1 Defining Variables
Variables are the containers in which we can store data in the memory and access it later.

In **Dino** we give users to define two types of container-

- Using *assign* keyword- Containers defined by this method can be reassigned with different values.
- Using *const* keyword- These containers have constant value and can not be reassigned with different values.

E.g.-

|<p>assign a = 3;</p><p>echo(a+5);</p>|<p>const a = 3;</p><p>echo(a+5);</p>|
| :- | :- |
#### <a name="_1v1zt2dthkog"></a>2.2 Scoping
The scoping of vaiiables in **Dino** is lexical scoping. The language does a resolution pass before evaluation to determine the mapping of which variable refers to which position.This helps us easily evaluate cases like-

*assign a = 5;*

*if(a>5)*

*assign a = 10;*

*echo(a);*

*end*

*else*

*assign a = 15;*

*echo(a);*

*end*

*echo(a); ? Outputs: 15 5*