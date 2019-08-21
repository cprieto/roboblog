---
title: Vectors, Arrays and NumPy
date: 2019-08-21
slug: vectors-arrays-and-numpy
tags: numpy, math, python
twitter_image: numpy_logo.jpg
---

[NumPy](https://www.numpy.org/) is a very powerful mathematical library for "crunching numbers" in Python, it has functions and modules for a lot of advance and not so advance mathematical operations, including [linear algebra](https://en.wikipedia.org/wiki/Linear_algebra).

Recently in classes we had been learning about vector and matrix operations, and most books include examples in things like [Matlab](https://en.wikipedia.org/wiki/MATLAB) or [Octave](https://en.wikipedia.org/wiki/GNU_Octave) so I was curious about how we can represent this in Python, so I decided to take a look and write this as a simple reminder of simple vector and basic operations in Python using NumPy. Of course I will assume you have already NumPy installed, if not, go to your closest [virtual environment](https://docs.python.org/3/tutorial/venv.html) and install it with a simple command (depending on your platform this could take _a while_):

```
pip install numpy
```

Later in our scripts we just need to import NumPy, and by convention we name the import as `np`

```python
import numpy as np
```

# Vectors

In normal mathematical notation we declare a vector in different ways, the most common (usually) is using a vertical matrix, something like this:
$$
\begin{pmatrix}1\\2\\3\end{pmatrix}
$$
Notice some books declare this vector using its _transpose_ version, $(1,2,3)^\top$.

Luckily for us, declaring a vector in NumPy is simple:

```python
np.array([1,2,3])
```
[]>
array([1, 2, 3])
<[]

Arrays in NumPy are super powerful, they are used to express not only vectors but matrices and multidimensional structures, they are very memory efficient and used extensively for mathematical operations.

# Matrices

In the same way, declaring the following 2x3 matrix:
$$
\begin{bmatrix}
1&2&3\\
4&5&6
\end{bmatrix}
$$
This can be easily done in NumPy with `np.array`, but notice we need to pass a _multidimensional list_ instead of just a simple list:

```python
np.array([[1,2,3], [4,5,6]])
```
[]>
array([[1, 2, 3],
       [4, 5, 6]])
<[]

Notice the usage of the same type of structure to represent arrays and matrices, this is what makes NumPy so powerful, in previous versions you have different operators for vectors and arrays, but this is not the case anymore in modern NumPy versions.

# Operations

We can use _common_ operations over existing matrices and vectors, for example, sum, subtraction and _scalar multiplication_.

```python
np.array([1,2,3]) + np.array([4,5,6])
5*np.array([[1,2,3], [4,5,6]])
```
[]>
array([5, 7, 9])
array([[ 5, 10, 15],
       [20, 25, 30]])
<[]

Matrix multiplication is a little tricky, you see, if you use the standard multiplication symbol `*` you will get a little surprise:

```python
np.array([[1,2,3], [4,5,6]]) * np.array([[2,4,6], [8,2,4]])
```
[]>
array([[ 5, 10, 15],
       [20, 25, 30]])
<[]

In this case, multiplication of two matrices is _element wise_ and known as [Hadamard product](https://en.wikipedia.org/wiki/Hadamard_product_(matrices)), the same happens with Vectors:

```python
np.array([1,2,3]) * np.array([2,4,6])
```
[]>
array([ 2,  8, 18])
<[]

But what if what you want is the _real_ matrix multiplication operation? Well, if you are using Python 3.5 or greater, you need to use the `__matmul__` operator `@` or (if you are, for some reason, using an earlier version of Python) `np.dot`

```python
a, b = np.array([[1,2,3], [4,5,6]]), np.array([[2,4], [6,8], [2,4]])
a @ b
np.dot(a, b)
```
[]>
array([[20, 32],
       [50, 80]])
array([[20, 32],
       [50, 80]])
<[]

Notice this is the equivalent of the _dot product_ of two vectors, so the same operation with vectors is just their dot product (or _inner product_):

```python
np.array([1, 2, 3]) @ np.array([4, 5, 6])
```
[]>
32
<[]

What about the _cross product_ of two vectors? Well, in this case we don't have a convinient operator as the dot product, but we have the function `np.cross`:

```python
a, b = np.array([1, 2, 3]), np.array([4, 5, 6])
np.cross(a, b)
```
[]>
array([-3,  6, -3])
<[]

# Convenient shortcuts

There are some "special" matrices and we can use special methods instead of create them directly using the `np.array` notation, for example, the _identity_ matrix

$$
\begin{bmatrix}
1&0&0\\
0&1&0\\
0&0&1\end{bmatrix}
$$

Can be created using `np.identity`

```python
np.identity(3)
```
[]>
array([[1., 0., 0.],
       [0., 1., 0.],
       [0., 0., 1.]])
<[]

Or a matrix full of zeroes:

```python
np.zeros((3,2))
```
[]>
array([[0., 0.],
       [0., 0.],
       [0., 0.]])
<[]

But maybe full of ones:

```python
np.ones((3,2))
```
[]>
array([[1., 1.],
       [1., 1.],
       [1., 1.]])
<[]

**Important**: Notice we pass the dimension in a _tuple_, not as a simple parameter, with the exception of `np.identity`, passing a single number will create a vector of that size, for example:"

```python
np.ones(3)
```
[]>
array([1, 1, 1])
<[]

# Special operations

We can _transpose_ a matrix as well easily using the method `transpose` in every `np.array` object:

```python
a = np.array([[1, 2], [3, 4]])
a.transpose()
```
[]>
array([[1, 2],
       [3, 4]])
<[]

Another two very common operations are the determinant of a matrix, for this we have the function `np.linalg.det`

```python
a = np.array([[12,23], [45,62]])
np.linalg.det(a)
```
[]>
-291.0000000000001
<[]

And our friend the inverse of a matrix, `np.linalg.inv`

```python
a = np.array([[12,23], [45,62]])
np.linalg.inv(a)
```
[]>
array([[-0.21305842,  0.0790378 ],
       [ 0.15463918, -0.04123711]])
<[]

As you can see, we can handle vector and matrix operations in Python using NumPy as easy as in any other language, there are a lot more of functions of NumPy just for [linear algebra](https://docs.scipy.org/doc/numpy/reference/routines.linalg.html) waiting there to explore, go and take a look, remember, Python is pure love!
